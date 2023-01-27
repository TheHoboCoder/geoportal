from django.views import View
from rest_framework.response import Response
from ..module_config import COMMANDS

class CommandView(View):
    # must set in subclass
    serializer_class = None

    def handler(self, validated_data):
        pass

    def get(self, request):
        serializer = self.serializer_class(data=request.GET)
        if serializer.is_valid(raise_exception=True):
            # TODO: this
            return Response(data=self.handler(serializer.validated_data))

def get_commands(request):
    return Response(data=COMMANDS.keys())
