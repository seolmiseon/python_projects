from langchain_upstage import ChatUpstage
import os

def get_solar_mini(api_key):
    return ChatUpstage(api_key=api_key, model="solar-mini")

def get_solar_pro(api_key):
    return ChatUpstage(api_key=api_key, model="solar-pro")