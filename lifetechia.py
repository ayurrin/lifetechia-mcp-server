import httpx
import os
from urllib.parse import urlencode
from mcp.server.fastmcp import FastMCP


# Initialize FastMCP server
mcp = FastMCP("edinet")

# Constants
API_URL = "https://lifetechia.com/wp-json/financial/v1/get/"
API_KEY = os.environ.get("API_KEY")


async def get_financial_data_from_api(company_name: str = None, sec_code: str = None, doc_id: str = None, start_date: str = None, end_date: str = None) -> str:
    """
    財務データを取得する関数

    Args:
        company_name (str, optional): 企業名
        sec_code (str, optional): 証券コード
        doc_id (str, optional): ドキュメントID
        start_date (str, optional): 開始日（YYYY-MM-DD）
        end_date (str, optional): 終了日（YYYY-MM-DD）

    Returns:
        pd.DataFrame: 取得したデータのデータフレームを文字列として返す
    """
    params = {}

    if not API_KEY:
        raise ValueError("API_KEY environment variable not set")

    if company_name:
        params["company_name"] = company_name

    if sec_code:
        if isinstance(sec_code, list):
            params["sec_code[]"] = sec_code  # リスト形式に対応
        else:
            params["sec_code"] = sec_code

    if doc_id:
        if isinstance(doc_id, list):
            params["doc_id[]"] = doc_id  # リスト形式に対応
        else:
            params["doc_id"] = doc_id

    if start_date:
        params["start_date"] = start_date

    if end_date:
        params["end_date"] = end_date

    # クエリパラメータをエンコード
    query_string = urlencode(params, doseq=True)
    final_url = f"{API_URL}?{query_string}" if params else API_URL  # パラメータがない場合はそのままアクセス

    # APIリクエスト用のヘッダー
    headers = {"X-API-Key": API_KEY}

    async with httpx.AsyncClient() as client:
        # APIリクエストの送信
        response = await client.get(final_url, headers=headers)

        # レスポンスの処理
        if response.status_code == 200:
            data = response.json()
            return data  
        else:
            print(
                "Error:",
                response.status_code,
                response.text.encode().decode("unicode_escape"),
            )
            return API_KEY, response.status_code # 空のデータフレームを返す


@mcp.tool()
async def get_financial_data_by_company_name(company_name: str, start_date: str = None, end_date: str = None) -> str:
    """
    企業名で財務データを取得するツール

    Args:
        company_name (str): 企業名
        start_date (str, optional): 開始日（YYYY-MM-DD）
        end_date (str, optional): 終了日（YYYY-MM-DD）

    Returns:
        str: 取得した財務データを文字列として返す
    """
    data = await get_financial_data_from_api(company_name=company_name, start_date=start_date, end_date=end_date)
    return str(data)


@mcp.tool()
async def get_financial_data_by_sec_code(sec_code: str, start_date: str = None, end_date: str = None) -> str:
    """
    証券コードで財務データを取得するツール

    Args:
        sec_code (str): 証券コード+0 （例: 72030）
        start_date (str, optional): 開始日（YYYY-MM-DD）
        end_date (str, optional): 終了日（YYYY-MM-DD）

    Returns:
        str: 取得した財務データを文字列として返す
    """
    data = await get_financial_data_from_api(sec_code=sec_code, start_date=start_date, end_date=end_date)
    return str(data)


@mcp.tool()
async def get_financial_data_by_doc_id(doc_id: str, start_date: str = None, end_date: str = None) -> str:
    """
    ドキュメントIDで財務データを取得するツール

    Args:
        doc_id (str): ドキュメントID'S100TR7I'など
        start_date (str, optional): 開始日（YYYY-MM-DD）
        end_date (str, optional): 終了日（YYYY-MM-DD）

    Returns:
        str: 取得した財務データを文字列として返す
    """
    data = await get_financial_data_from_api(doc_id=doc_id, start_date=start_date, end_date=end_date)
    return str(data)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
