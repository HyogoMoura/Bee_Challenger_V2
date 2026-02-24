import requests
import pandas as pd
from time import sleep
from datetime import datetime
import os
import logging

# =========================
# CONFIGURAÇÃO
# =========================
BASE_URL = "https://api.openbrewerydb.org/v1/breweries"
PER_PAGE = 200
TIMEOUT = 10
SLEEP_BETWEEN_CALLS = 0.2
OUTPUT_PATH = "raw_output/breweries.parquet"


# =========================
# LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# =========================
# FUNÇÃO PRINCIPAL
# =========================
def fetch_all_breweries(max_pages=None):
    session = requests.Session()
    all_pages = []
    page = 1

    while True:
        try:
            logger.info(f"Buscando página {page}...")

            params = {"page": page, "per_page": PER_PAGE}
            resp = session.get(BASE_URL, params=params, timeout=TIMEOUT)
            resp.raise_for_status()

            data = resp.json()

            if not isinstance(data, list):
                raise ValueError("Resposta inesperada da API.")

            if not data:
                logger.info("Paginação encerrada.")
                break

            all_pages.append(pd.DataFrame(data))

            if max_pages and page >= max_pages:
                logger.info("Limite de páginas atingido.")
                break

            page += 1
            sleep(SLEEP_BETWEEN_CALLS)

        except requests.RequestException as e:
            logger.error(f"Erro na requisição: {e}")
            raise

    if all_pages:
        df = pd.concat(all_pages, ignore_index=True)
    else:
        df = pd.DataFrame()

    return df


# =========================
# EXECUÇÃO
# =========================
def main():
    logger.info("Iniciando ingestão Bronze...")

    df = fetch_all_breweries()

    logger.info(f"Total de registros coletados: {len(df)}")

    if df.empty:
        logger.warning("DataFrame vazio. Nada será salvo.")
        return

    # Adiciona coluna de ingestão
    df["ingestion_timestamp"] = datetime.utcnow()

    # Cria pasta se não existir
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    df.to_parquet(OUTPUT_PATH, index=False)

    logger.info(f"Arquivo salvo em: {OUTPUT_PATH}")
    logger.info("Ingestão finalizada com sucesso.")


if __name__ == "__main__":
    main()