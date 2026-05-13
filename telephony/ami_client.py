from loguru import logger
from config.settings import get_settings


class AMIClient:
    """
    Cliente AMI (Asterisk Manager Interface).
    En producción usa panoramisk para conexión real.
    Actualmente opera en modo simulación.
    """

    def __init__(self):
        settings = get_settings()
        self.host = settings.ami_host
        self.port = settings.ami_port
        self.username = settings.ami_username
        self.secret = settings.ami_secret
        self._connected = False

    async def connect(self):
        """Conecta al servidor AMI de Asterisk."""
        try:
            # TODO: Integrar panoramisk para conexión real
            # from panoramisk import Manager
            # self._manager = Manager(
            #     host=self.host, port=self.port,
            #     username=self.username, secret=self.secret
            # )
            # await self._manager.connect()
            logger.info(f"AMI Client: modo simulación (target: {self.host}:{self.port})")
            self._connected = True
        except Exception as e:
            logger.error(f"Error conectando a AMI: {e}")
            self._connected = False

    async def disconnect(self):
        self._connected = False
        logger.info("AMI Client desconectado")

    async def transfer(self, channel: str, extension: str, context: str = "from-internal"):
        """
        Transfiere una llamada usando AMI Action: Redirect
        En producción ejecutaría:
            Action: Redirect
            Channel: {channel}
            Context: {context}
            Exten: {extension}
            Priority: 1
        """
        if not self._connected:
            logger.warning("AMI no conectado, transferencia simulada")

        logger.info(f"AMI Redirect: Channel={channel} -> Exten={extension} Context={context}")

        # TODO: Implementación real con panoramisk:
        # response = await self._manager.send_action({
        #     'Action': 'Redirect',
        #     'Channel': channel,
        #     'Context': context,
        #     'Exten': extension,
        #     'Priority': '1'
        # })
        # return response

        return {"Response": "Success", "Message": f"Redirect sent (simulated) to {extension}"}

    async def hangup(self, channel: str, cause: int = 16):
        """Cuelga un canal específico."""
        logger.info(f"AMI Hangup: Channel={channel} Cause={cause}")

        # TODO: Implementación real:
        # response = await self._manager.send_action({
        #     'Action': 'Hangup',
        #     'Channel': channel,
        #     'Cause': str(cause)
        # })

        return {"Response": "Success", "Message": f"Hangup sent (simulated) for {channel}"}

    async def originate(self, extension: str, context: str = "from-internal",
                        caller_id: str = "Nova <*999>"):
        """Origina una nueva llamada."""
        logger.info(f"AMI Originate: Exten={extension} CallerID={caller_id}")
        return {"Response": "Success", "Message": f"Originate sent (simulated) to {extension}"}

    @property
    def is_connected(self) -> bool:
        return self._connected
