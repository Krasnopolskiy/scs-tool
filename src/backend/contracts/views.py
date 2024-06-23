import asyncio
import json
from argparse import Namespace

from django.http import Http404
from django.shortcuts import render
from django.views import View
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.contracts.models import Contract, Report
from backend.contracts.serializers import ContractSerializer
from cli.executors import scan, analyze
from common.constants import SOURCE_PATH
from common.schemas import Address

ARGS = Namespace(
    etherscan=True,
    semgrep=True,
    openai=True,
    mythril=True,
    slither=True,
    decompile=False,
)


class IndexView(View):
    def get(self, request: Request):
        return render(request, "contracts.html")


class ContractView(View):
    def get(self, request: Request, address: str):
        contract = get_object_or_404(Contract, address=address)
        return render(request, "contracts.html", {"contract": contract})


class ContractAPIView(APIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def get(self, request: Request, address: str):
        contract = get_object_or_404(self.queryset, address=address)
        return Response(ContractSerializer(contract).data)

    def post(self, request: Request, address: str):
        try:
            return self.get(request, address)
        except Http404:
            pass
        self.full_analyze(ARGS, address)
        self.load_analyze_results(address)
        return self.get(request, address)

    def full_analyze(self, args: Namespace, address: Address):
        asyncio.run(scan(args, [address]))
        asyncio.run(analyze(args, [address]))

    def load_analyze_results(self, address: Address):
        directory = SOURCE_PATH / address
        contracts = [contract.read_text() for contract in directory.rglob("*.sol")]

        reports = list(directory.rglob("*.json"))

        contract = Contract.objects.create(
            address=address,
            source="\n".join(contracts),
        )

        for report in reports:
            content = report.read_text()
            Report.objects.create(
                contract=contract,
                report=json.loads(content),
                analyzer=report.name.removesuffix(".json"),
            )
