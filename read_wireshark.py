import typing
import pyshark
import socket
from ipwhois import IPWhois, ipwhois


def translate_addr(ip: str) -> str | bool:
    """
    Traduz o endereço ip para o nome do dominio associado
    :param ip: str -> 192.0.0.0.1
    :return: www.google.com
    """
    try:
        obj = IPWhois(ip)
        results = obj.lookup_rdap()
        return results['asn_description']
    except ipwhois.exceptions.IPDefinedError:
        return False


def get_ip() -> str:
    """Obtem endereço ip local"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except socket.error:
        return "Falha ao conectar-se a rede"


def get_router() -> str:
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        return "Falha ao obter informações de rede"


def reader(file_path: str) -> typing.Set[typing.Any]:
    """
    Le arquivo .pcap extraído do wireshark com os filtros do dia
    :param file_path: str -> local do arquivo
    :return: dict -> hosts e quantidades de acesso no período
    """
    store: typing.Set[typing.Any] = set()
    local_ip_address: str = get_ip()
    counter: int = 0
    gateway_ip_address: str = get_router()
    cap: typing.Any = pyshark.FileCapture(file_path)
    for packet in cap:
        try:
            if 'http' in packet:
                if str(packet.ip.src) != local_ip_address and str(packet.ip.src) != gateway_ip_address:
                    ip_dst = packet.ip.src
                    timestamp = packet.sniff_time
                    store.add(f"{ip_dst} + {timestamp}")
        except AttributeError:
            ...
    return store

