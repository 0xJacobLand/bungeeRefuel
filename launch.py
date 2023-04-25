import json
import random
import time
from web3 import Web3
from web3.middleware import geth_poa_middleware

# Установка соединения с RPC-узлом Arbitrum One
arb_rpc_url = "https://arb1.arbitrum.io/rpc"
web3_arbitrum = Web3(Web3.HTTPProvider(arb_rpc_url))

# Установка соединения с RPC-узлом Polygon нахуй не надо, на будущее
polygon_rpc_url = "https://rpc-mainnet.maticvigil.com/"
web3_polygon = Web3(Web3.HTTPProvider(polygon_rpc_url))

# Адрес контракта и загрузка ABI банги из файла
contract_address = Web3.to_checksum_address('0xc0e02aa55d10e38855e13b64a8e1387a04681a00')
with open('abi.txt', 'r') as file:
    abi = json.load(file)

# Получение экземпляра контракта с помощью ABI и адреса контракта
contract = web3_arbitrum.eth.contract(address=contract_address, abi=abi)

# Добавление middleware
web3_arbitrum.middleware_onion.inject(geth_poa_middleware, layer=0)

# Настройка параметров транзакции
gas_price = web3_arbitrum.eth.gas_price
gas_limit = 1000000

with open('private.txt') as f:
    for private_key in f:
        private_key = private_key.strip()
        account = web3_arbitrum.eth.account.from_key(private_key)
        nonce = web3_arbitrum.eth.get_transaction_count(account.address)
        your_address = account.address

        # Определение сети пополнения, 137 polygon, 250  fantom, 56 BSC, 43114 AVAX
        chain_id = 43114

        # Выбор случайного значения между переводом, проверить руками на банги мин-макс
        amount_ether = random.uniform(0.002300, 0.002400)

        # Преобразование суммы в wei
        amount_wei = web3_arbitrum.to_wei(amount_ether, 'ether')

        # Настройка параметров транзакции
        gas_price = web3_arbitrum.eth.gas_price
        gas_limit = 1000000

        # Вызов функции depositNativeToken и отправка транзакции
        tx = contract.functions.depositNativeToken(
            chain_id, your_address
        ).build_transaction({
            'from': account.address,
            'nonce': nonce,
            'gas': gas_limit,
            'gasPrice': gas_price,
            'chainId': 42161,
            'value': amount_wei
        })

        signed_tx = web3_arbitrum.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = web3_arbitrum.eth.send_raw_transaction(signed_tx.rawTransaction)

        # Ожидание подтверждения транзакции
        #tx_receipt = web3_arbitrum.eth.wait_for_transaction_receipt(tx_hash)
        print(account.address, "done")

        # Добавление случайной задержки перед переходом к следующему приватному ключу
        time.sleep(random.uniform(1, 7))
