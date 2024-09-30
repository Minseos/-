import os
import yfinance as yf
import pandas as pd
from tqdm import tqdm
from stqdm import stqdm

from datetime import datetime
from yahoo_fin import stock_info as si
import itertools
# import talib as ta

class Ticker:
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder

class TickerSaver(Ticker):
    def __init__(self, data_folder="data", nasdaq=True, dow=False):
        super().__init__(data_folder=data_folder)
        self.create_data_folder()
        self.failed_tickers = []
        self.create_tickers(nasdaq, dow)

    def create_tickers(self, nasdaq=True, dow=False):
        self.tickers = []
        remove_ticker = ['AAGRW','ABLLW','ABLVW','ABVEW','ACABW','ACACW','ACONW','ADNWW','ADSEW','ADVWW','AEAEW','AENTW','AERTW','AFJKR','AFRIW','AGBAW','AILEW','AIMAW','AIMDW','AIRJW','AISPW','AITRR','ALCYW','ALFUW','ALSAR','ALSAW','ALVOW','ANGHW','ANSCW','APCXW','APXIW','AQUNR','ARBEW','AREBW','ARKOW','ASCBR','ASCBW','ASTLW','ASTSW','ATMCR','ATMCW','ATMVR','ATNFW','AUROW','AUUDW','AVPTW','BAERW','BAYAR','BCGWW','BCSAW','BCTXW','BEATW','BENFW','BETRW','BFIIW','BFRGW','BFRIW','BHACW','BIAFW','BKHAR','BLACR','BLACW','BLDEW','BLEUR','BLEUW','BNAIW','BNIXR','BNIXW','BNZIW','BOCNW','BOWNR','BRACR','BRKHW','BRLSW','BROGW','BSLKW','BTBDW','BTCTW','BTMWW','BUJAR','BUJAW','BYNOW','BZFDW','CAPTW','CCIXW','CCTSW','CDAQW','CDIOW','CDROW','CDTTW','CEADW','CELUW','CEROW','CFFSW','CGBSW','CIFRW','CINGW','CITEW','CLNNW','CLRCR','CLRCW','CMAXW','CMPOW','COCHW','COEPW','COOTW','CORZW','CORZZ','CPTNW','CRESW','CREVW','CRGOW','CRMLW','CSLMR','CSLMW','CSLRW','CTCXW','CUBWW','CURIW','CXAIW','DAVEW','DBGIW','DECAW','DFLIW','DHAIW','DHCNL','DISTR','DISTW','DPCSW','DRMAW','DRTSW','DSYWW','DTSQR','DTSTW','DUETW','DYCQR','ECDAW','ECXWW','EDBLW','EMCGR','EMCGW','ENGNW','ESGLW','ESHAR','ESLAW','EUDAW','EURKR','EVGRW','EVLVW','FAASW','FATBW','FBYDW','FFIEW','FGIWW','FIACW','FLDDW','FMSTW','FNVTW','FORLW','FSHPR','FTIIW','FUFUW','GBBKR','GBBKW','GCMGW','GDEVW','GDSTR','GDSTW','GECCZ','GFAIW','GGROW','GHIXW','GIGGW','GIPRW','GLACR','GLLIR','GLLIW','GLSTR','GLSTW','GODNR','GOEVW','GOVXW','GPATW','GRDIW','GRRRW','GSMGW','GTACW','HAIAW','HCVIW','HHGCR','HHGCW','HOFVW','HOLOW','HOVRW','HPAIW','HSCSW','HSPOR','HSPOW','HTZWW','HUBCW','HUBCZ','HUMAW','HYMCW','HYZNW','IBACR','ICUCW','IGTAR','IGTAW','IMTXW','INTEW','INVZW','IPXXW','IROHR','IROHW','ISRLW','IVCAW','IVCBW','IVCPW','IVDAW','IXAQW','JFBRW','JMID','JSPRW','JVSAR','KACLR','KACLW','KDLYW','KITTW','KLTOW','KPLTW','KTTAW','KVACW','KWESW','LCFYW','LDTCW','LEXXW','LFLYW','LGHLW','LIFWZ','LIVR','LNZAW','LOTWW','LPAAW','LSBPW','LSEAW','LTRYW','LUNRW','LVROW','MACIW','MAPSW','MARXR','MCAAW','MCAGR','MDAIW','MITAW','MKDWW','MLECW','MMVWW','MNTSW','MOBXW','MRNOW','MSAIW','MSSAR','MSSAW','MTEKW','MVSTW','NCNCW','NCPLW','NEOVW','NETDW','NIOBW','NIVFW','NKGNW','NMHIW','NNAVW','NOVVR','NOVVW','NPABW','NRSNW','NRXPW','NVACR','NVACW','NVAWW','NVNIW','NVVEW','NWTNW','NXGLW','NXLIW','NXPLW','OABIW','OAKUW','OCEAW','OCSAW','ODVWZ','ONFOW','ONMDW','ONYXW','OPTXW','ORGNW','OXBRW','PAVMZ','PAYOW','PBMWW','PCTTW','PETWW','PFTAW','PIIIW','PITAW','PLAOW','PLMJW','PPYAW','PRENW','PRLHW','PROCW','PTIXW','PWUPW','PXSAW','QETAR','QOMOR','QOMOW','QSIAW','RCKTW','RCRTW','RDZNW','RELIW','REVBW','RFACR','RFACW','RFAIR','RGTIW','RMCOW','ROCLW','RUMBW','RVMDW','RVPHW','RVSNW','RZLVW','SABSW','SAIHW','SATLW','SBC','SBCWW','SBFMW','SCLXW','SDAWW','SDSTW','SHFSW','SHMDW','SHOTW','SIMAW','SLDPW','SLXNW','SMXWW','SNAXW','SONDW','SOUNW','SPKLW','SQFTW','SRZNW','STSSW','SURGW','SVIIR','SVIIW','SVMHW','SVREW','SWAGW','SWVLW','SXTPW','SYTAW','TALKW','TBLAW','TCBPW','TETEW','TGAAW','THCPW','TLGYW','TMTCR','TNONW','TOIIW','TVGNW','UHGWW','UKOMW','USGOW','VEEAW','VGASW','VMCAW','VRMEW','VSACW','VSEEW','VSTEW','WAVSW','WESTW','WGSWW','WINVR','WINVW','WLDSW','WTMAR','XBPEW','XFINW','XOSWW','YHNAU','YOTAR','YOTAW','ZAPPW','ZAZZT','ZBZZT','ZCARW','ZCZZT','ZEOWW','ZJZZT','ZOOZW','ZPTAW','ZVZZT','ZWZZT','ZXYZ.A','ZXZZT']

        if nasdaq:
            # 나스닥(NASDAQ)의 티커 목록 가져오기
            self.tickers.append(si.tickers_nasdaq())

        if dow:
            # 다우 존스(Dow Jones)의 티커 목록 가져오기
            self.tickers.append(si.tickers_dow())

        if self.tickers:
            # 전체 티커 목록 가져오기
            self.tickers = list(itertools.chain(*self.tickers))
            self.tickers = [t for t in self.tickers if t not in remove_ticker]
        else:
            print("가져온 ticker가 없습니다.")

    def create_data_folder(self):
        # 데이터 저장 폴더가 없으면 생성
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

    def get_last_date_from_filename(self, filename):
        # 파일 이름에서 마지막 날짜 추출
        try:
            date_str = filename.split("_")[-1].split(".")[0]
            return datetime.strptime(date_str, "%Y_%m_%d")
        except Exception as e:
            print(f"Error parsing date from filename {filename}: {e}")
            return None
        
    def add_indicators(self, df):
        # SMA 추가
        df['SMA_5'] = ta.SMA(df['Close'], timeperiod=5)
        df['SMA_10'] = ta.SMA(df['Close'], timeperiod=10)
        df['SMA_20'] = ta.SMA(df['Close'], timeperiod=20)
        df['SMA_50'] = ta.SMA(df['Close'], timeperiod=50)
        df['SMA_100'] = ta.SMA(df['Close'], timeperiod=100)
        df['SMA_200'] = ta.SMA(df['Close'], timeperiod=200)
        
        # RSI 추가
        df['RSI_14'] = ta.RSI(df['Close'], timeperiod=14)
        
        # MACD 추가
        df['MACD'], df['MACD_signal'], df['MACD_hist'] = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        
        # Bollinger Bands 추가
        df['BB_upper'], df['BB_middle'], df['BB_lower'] = ta.BBANDS(df['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        
        # Stochastic Oscillator 추가
        df['STOCH_k'], df['STOCH_d'] = ta.STOCH(df['High'], df['Low'], df['Close'], fastk_period=14, slowk_period=3, slowd_period=3)
        
        return df
    
    def save_data_to_csv(self, ticker, data):
        # 데이터의 마지막 날짜를 기준으로 파일명 생성
        last_date = data.index[-1].strftime("%Y_%m_%d")
        filename = f"{self.data_folder}/{ticker}_{last_date}.csv"

        data = self.add_indicators(data)
        data["ticker"] = ticker
        
        # 데이터 CSV로 저장
        data.to_csv(filename)
    
    def update_existing_file(self, ticker, existing_file, new_data):
        # 기존 파일에서 데이터 읽기
        existing_data = pd.read_csv(existing_file, index_col='Date', parse_dates=True)
        
        # 새로운 데이터와 병합
        combined_data = pd.concat([existing_data, new_data]).drop_duplicates()

        # 병합한 데이터 다시 저장
        self.save_data_to_csv(ticker, combined_data)
    
    def fetch_and_save_ticker_data(self, ticker):
        # 이미 저장된 파일 체크
        existing_files = [f for f in os.listdir(self.data_folder) if f.startswith(ticker) and f.endswith('.csv')]

        if existing_files:  # 파일이 있을 경우
            try:
                # 가장 최근 파일 찾기
                latest_file = max(existing_files, key=self.get_last_date_from_filename)
                last_date = self.get_last_date_from_filename(latest_file)
                
                # 파일에 있는 마지막 날짜 이후의 데이터만 가져오기
                start_date = pd.Timestamp(last_date + pd.Timedelta(days=1)).tz_localize('UTC')
                new_data = yf.download(ticker, start=start_date, progress=False)
                
                if not new_data.empty:
                    self.update_existing_file(ticker, f"{self.data_folder}/{latest_file}", new_data)
                else:
                    self.failed_tickers.append(ticker)
            except Exception as e:
                print(f"Error updating {ticker}: {e}")
                self.failed_tickers.append(ticker)
        else:  # 처음 데이터를 가져와 저장할 때
            try:
                data = yf.download(ticker, progress=False)
                if not data.empty:
                    self.save_data_to_csv(ticker, data)
                else:
                    self.failed_tickers.append(ticker)
            except Exception as e:
                print(f"Error downloading {ticker}: {e}")
                self.failed_tickers.append(ticker)
    
    def save_all_tickers_data(self):
        for ticker in tqdm(self.tickers):
            self.fetch_and_save_ticker_data(ticker)


class TickerLoader(Ticker):
    def __init__(self, data_folder="data"):
        super().__init__(data_folder=data_folder)
    
    def get_data(self, min_days=1000, streamlit_tqdm=False):
        file_list = os.listdir(self.data_folder)
        if streamlit_tqdm:
            dfs = [pd.read_csv(f"{self.data_folder}/{f}") 
                   for f in stqdm(file_list, desc="Load stock data")]
        else:
            dfs = [pd.read_csv(f"{self.data_folder}/{f}") for f in tqdm(file_list)]
        df = pd.concat(dfs)
        df.dropna(inplace=True)
        del dfs
        
        return self.filter_tickers_by_row_count(df, min_days)

    def filter_tickers_by_row_count(self, df, min_days=1000):
        # 티커별 row 개수 계산
        ticker_counts = df['ticker'].value_counts()
        
        # min_days개 이상인 티커만 필터링
        valid_tickers = ticker_counts[ticker_counts >= min_days].index
        
        # 유효한 티커만 포함한 데이터프레임 반환
        filtered_df = df[df['ticker'].isin(valid_tickers)]
        
        return filtered_df
