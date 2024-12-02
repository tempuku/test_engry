from pydantic import BaseModel, Field, IPvAnyAddress


class ServerInfo(BaseModel):
    add_time: int = Field(
        ..., alias="addTime", description="Timestamp when the server was added."
    )
    ip: IPvAnyAddress = Field(..., description="IP address of the server.")
    port: int = Field(..., gt=0, lt=65536, description="Port number (1-65535).")
    country: str = Field(..., description="Country code.")
    ping: int = Field(
        ..., gt=0, description="Ping time in milliseconds (must be positive)."
    )

    def get_link(self):
        return f"socks5://{self.ip}:{self.port}"
