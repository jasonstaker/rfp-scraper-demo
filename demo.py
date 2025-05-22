import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import parse_qsl, urlencode
from io import StringIO

STATE_RFP_URL = 'https://app.az.gov/page.aspx/en/rfp/request_browse_public'
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    ),
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": STATE_RFP_URL
}
FALLBACK_CSRF = "4b9qnD7UgwevuI79WCsBUAv2VtsgEvdqW8gdWmgRSO0%3D"
KEYWORD_FILE = 'config/keywords.txt'

def _scrape_hidden_fields(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    hidden_inputs = {}

    for hidden in soup.find_all("input", type="hidden"):
        name = hidden.get("name")
        value = hidden.get("value", "")
        if name:
            hidden_inputs[name] = value

    return hidden_inputs


def build_search_payload(hidden_fields):
    data = {**hidden_fields}

    data["hdnUserValue"] = "%2Cbody_x_txtRfpAwarded_1"
    data["__LASTFOCUS"] = "body_x_prxFilterBar_x_cmdSearchBtn"
    data["__EVENTTARGET"] = "body:x:prxFilterBar:x:cmdSearchBtn"
    data["__EVENTARGUMENT"] = ""
    data["HTTP_RESOLUTION"] = ""
    data["REQUEST_METHOD"] = "POST"
    data["header:x:prxHeaderLogInfo:x:ContrastModal:chkContrastTheme_radio"] = "true"
    data["header:x:prxHeaderLogInfo:x:ContrastModal:chkContrastTheme"] = "True"
    data["x_headaction"] = ""
    data["x_headloginName"] = ""
    data["header:x:prxHeaderLogInfo:x:ContrastModal:chkPassiveNotification"] = "0"
    data["proxyActionBar:x:txtWflRefuseMessage"] = ""
    data["hdnMandatory"] = "0"
    data["hdnWflAction"] = ""
    data["body:_ctl0"] = ""
    data["body:x:txtQuery"] = ""
    data["body_x_selFamily_text"] = ""
    data["body:x:selFamily"] = ""
    data["body:x:prxFilterBar:x:cmdSearchBtn"] = ""
    data["body:x:prxFilterBar:x:hdnResetFilterUrlbody_x_prxFilterBar_x_cmdRazBtn"] = ""
    data["body_x_selRfptypeCode_text"] = ""
    data["body:x:selRfptypeCode"] = ""
    data["body_x_selStatusCode_1_text"] = ""
    data["body:x:selStatusCode_1"] = ""
    data["body:x:txtRfpBeginDate"] = ""
    data["body:x:txtRfpBeginDatemax"] = ""
    data["body_x_txtRfpAwarded_1_text"] = ""
    data["body:x:txtRfpAwarded_1"] = "False"
    data["body_x_selOrgaLevelOrgaNode_78E9FF04_1_text"] = ""
    data["body:x:selOrgaLevelOrgaNode_78E9FF04_1"] = ""

    tr_checks = [
        "body:x:grid:grd:tr_2884:ctrl_txtRfpAwarded=False",
        "body:x:grid:grd:tr_2001:ctrl_txtRfpAwarded=False",
        "body:x:grid:grd:tr_1997:ctrl_txtRfpAwarded=False",
        "body:x:grid:grd:tr_1971:ctrl_txtRfpAwarded=False",
        "body:x:grid:grd:tr_1969:ctrl_txtRfpAwarded=False",
        "body:x:grid:grd:tr_1964:ctrl_txtRfpAwarded=False",
        "body:x:grid:grd:tr_1955:ctrl_txtRfpAwarded=False",
        "body:x:grid:grd:tr_1950:ctrl_txtRfpAwarded=False",
        "body:x:grid:grd:tr_1931:ctrl_txtRfpAwarded=False",
        "body:x:grid:grd:tr_1927:ctrl_txtRfpAwarded=False",
        "body:x:grid:grd:tr_1921:ctrl_txtRfpAwarded=False",
        "body:x:grid:grd:tr_1912:ctrl_txtRfpAwarded=False",
        "body:x:grid:grd:tr_1910:ctrl_txtRfpAwarded=False",
        "body:x:grid:grd:tr_1903:ctrl_txtRfpAwarded=False",
        "body:x:grid:grd:tr_1893:ctrl_txtRfpAwarded=False",
    ]
    for entry in tr_checks:
        key, val = entry.split("=", 1)
        data[key] = val

    data["hdnSortExpressionbody_x_grid_grd"] = ""
    data["hdnSortDirectionbody_x_grid_grd"] = ""
    data["hdnCurrentPageIndexbody_x_grid_grd"] = "0"
    data["hdnRowCountbody_x_grid_grd"] = "100"
    data["maxpageindexbody_x_grid_grd"] = "6"
    data["ajaxrowsiscountedbody_x_grid_grd"] = "True"

    if "CSRFToken" in hidden_fields:
        data["CSRFToken"] = hidden_fields["CSRFToken"]
    else:
        data["CSRFToken"] = FALLBACK_CSRF

    return urlencode(data, safe=':/|%')


def build_pagination_payload(page_num, hidden_fields):
    focus_idx = page_num - 1
    arg_idx = page_num - 1
    curr_idx = page_num - 2

    data = {
        "__LASTFOCUS": f"body_x_grid_PagerBtn{focus_idx}Page",
        "__EVENTTARGET": "body_x_grid_grd",
        "__EVENTARGUMENT": f"Page|{arg_idx}",
        **hidden_fields
    }

    data["hdnCurrentPageIndexbody_x_grid_grd"] = str(curr_idx)

    extras = {
        "hdnUserValue": "",
        "HTTP_RESOLUTION": "",
        "REQUEST_METHOD": "GET",
        "header:x:prxHeaderLogInfo:x:ContrastModal:chkContrastTheme_radio": "true",
        "header:x:prxHeaderLogInfo:x:ContrastModal:chkContrastTheme": "True",
        "x_headaction": "",
        "x_headloginName": "",
        "header:x:prxHeaderLogInfo:x:ContrastModal:chkPassiveNotification": "0",
        "proxyActionBar:x:txtWflRefuseMessage": "",
        "hdnMandatory": "0",
        "hdnWflAction": "",
        "body:_ctl0": "",
        "body:x:txtQuery": "",
        "body_x_selFamily_text": "",
        "body:x:selFamily": "",
        "body:x:prxFilterBar:x:hdnResetFilterUrlbody_x_prxFilterBar_x_cmdRazBtn": "",
        "body_x_selRfptypeCode_text": "",
        "body:x:selRfptypeCode": "",
        "body_x_selStatusCode_1_text": "",
        "body:x:selStatusCode_1": "",
        "body:x:txtRfpBeginDate": "",
        "body:x:txtRfpBeginDatemax": "",
        "body_x_txtRfpAwarded_1_text": "",
        "body:x:txtRfpAwarded_1": "",
        "body_x_selOrgaLevelOrgaNode_78E9FF04_1_text": "",
        "body:x:selOrgaLevelOrgaNode_78E9FF04_1": "",
        "hdnSortExpressionbody_x_grid_grd": "",
        "hdnSortDirectionbody_x_grid_grd": "",
        "hdnRowCountbody_x_grid_grd": hidden_fields.get("hdnRowCountbody_x_grid_grd", ""),
        "maxpageindexbody_x_grid_grd": hidden_fields.get("maxpageindexbody_x_grid_grd", ""),
        "ajaxrowsiscountedbody_x_grid_grd": hidden_fields.get("ajaxrowsiscountedbody_x_grid_grd", "False"),
    }

    if "CSRFToken" in hidden_fields:
        extras["CSRFToken"] = hidden_fields["CSRFToken"]
    else:
        extras["CSRFToken"] = FALLBACK_CSRF

    for k, v in extras.items():
        if k not in data:
            data[k] = v

    return urlencode(data, safe=":/|%")


def search_and_paginate_rfps():
    session = requests.Session()
    session.headers.update(HEADERS)

    resp0 = session.get(STATE_RFP_URL)
    if resp0.status_code != 200:
        print("Initial GET failed:", resp0.status_code)
        return pd.DataFrame()

    hidden = _scrape_hidden_fields(resp0.text)

    payload_search = build_search_payload(hidden)
    payload_dict = dict(parse_qsl(payload_search))

    resp_search = session.post(STATE_RFP_URL, data=payload_dict)
    if resp_search.status_code != 200:
        print("Search POST failed:", resp_search.status_code)
        return pd.DataFrame()

    hidden = _scrape_hidden_fields(resp_search.text)

    dfs = []
    try:
        df_page1 = pd.read_html(StringIO(resp_search.text))[4].reset_index(drop=True)
        dfs.append(df_page1)
    except Exception:
        print("No table found on search results (page 1).")
        return pd.DataFrame()

    page_num = 2
    while True:
        payload_page = build_pagination_payload(page_num, hidden)
        payload_dict = dict(parse_qsl(payload_page))

        resp_page = session.post(STATE_RFP_URL, data=payload_dict)
        if resp_page.status_code != 200:
            break

        new_hidden = _scrape_hidden_fields(resp_page.text)
        if not new_hidden.get("__VIEWSTATE"):
            break
        hidden = new_hidden

        try:
            df_next = pd.read_html(StringIO(resp_page.text))[4].reset_index(drop=True)
        except Exception:
            break

        if df_next.equals(dfs[-1]):
            break

        dfs.append(df_next)
        page_num += 1

    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)


def filter_by_keywords(df, keyword_file_path=KEYWORD_FILE):
    try:
        with open(keyword_file_path, 'r', encoding='utf-8') as f:
            keywords = [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Keyword file not found at path: {keyword_file_path}")
        return pd.DataFrame()

    if "Label" not in df.columns:
        print("Error: no 'Label' column found in scraped table.")
        return pd.DataFrame()

    matched = []
    for _, row in df[df['Label'].notna()].iterrows():
        lbl = row['Label'].lower()
        for kw in keywords:
            if kw in lbl:
                matched.append(row.to_dict())
                break

    return pd.DataFrame(matched)

def main():
    all_pages_df = search_and_paginate_rfps()
    if all_pages_df.empty:
        print("No RFP data retrieved (search or pagination returned no tables).")
        return

    matched_df = filter_by_keywords(all_pages_df)
    if matched_df.empty:
        print("No matches found for your keywords.")
    else:
        print(matched_df.drop_duplicates(subset='Code'))

if __name__ == "__main__":
    main()
