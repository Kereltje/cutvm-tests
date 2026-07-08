
"""
App home page: https://freeview.bsd.client.streaming.channel4.com/webapp/index.html
           or: https://google.bsd.client.streaming.channel4.com/webapp/index.html
User agent strings from https://assets.bsd.client.streaming.channel4.com/common/uaInjector.js
Keys, client (vodStreamClient), platform and device_group from https://config.bsd.client.streaming.channel4.com/26.3.0/{platform}/config.json
device_model from x-c4-device-name header and request payload to https://monitor.channel4.com/logs/client/bsd/{platform}?err
api_key from Authentication request header in https://api.channel4.com/online/v2/auth/token?client={client}
allowed_client from the error response to an api request (other than login, refresh, or revoke) with an invalid
client in the query string.

Everything is tested using Vivaldi and/or Firefox. Some devices only work on a Chrome based browser and some don't work
at all in a browser. The results may vary on real hardware. Refer to config.json for all possible variations on each
platform. Although not extensively tested, the api_keys produced by Vivaldi and Firefox appear to be the same for the
same device.
"""

from typing import TypedDict

# All allowed clients
allowed_clients = ['c4', 'ios', 'xbox', 'ps', 'wp8', 'xboxone', 'roku', 'freesat', 'android',
                   'samsung', 'win8', 'fvc', 'yvweb', 'cast', 'amazonfire', 'android-mod',
                   'fvp', 'samsung-dash', 'virginall4', 'yvdash', 'samsungorsay', 'xbox-dash',
                   'xboxone-dash', 'roku-dash', 'amazonfire-dash', 'ps-dash', 'cast-dash',
                   'skyoverip', 'googletv']


class DeviceData(TypedDict):
    user_agent: str
    api_key: str
    client: str
    platform: str
    device_model: str
    device_group: str
    keys: dict[str, dict[str, str]]


devices: dict[str, DeviceData] = {
    'amazon-fos5': {
        'user_agent': 'Mozilla/5.0 (Linux; Android 5.1.1; AFTT Build/LVY48F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.220 Mobile Safari/537.36 All4/7.4.0-release)',
        'api_key': 'eUExTHB6dGtHZUhaRDZuU2E3QzFBQUY2dkhwelZOblU6UXFFbUVnVVVVT1hUa3piNg==',
        'client': 'amazonfire-dash',
        'platform': 'amazonfire',
        'device_model': 'AFTT',
        'device_group': 'console',
        "keys": {
            "dash": {
                "iv": "B3LKVU05F3IDLVME",
                "key": "aYzHSI2iNhH2UyKdwjNHhAE7tasYEekhvMRBylKNmEQ="
            },
            "default": {
                "iv": "B3LKVU05F3IDLVME",
                "key": "aYzHSI2iNhH2UyKdwjNHhAE7tasYEekhvMRBylKNmEQ="
            }
        },
    },
    'amazon-fos6': {
        'user_agent': 'Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6705; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/118.0.0.0 Mobile Safari/537.36 All4/7.4.0-release)',
        'api_key': 'eUExTHB6dGtHZUhaRDZuU2E3QzFBQUY2dkhwelZOblU6UXFFbUVnVVVVT1hUa3piNg==',
        'client': 'amazonfire-dash',
        'platform': 'amazonfire',
        'device_model': 'AFTMM',
        'device_group': 'console',
        "keys": {
            "dash": {
                "iv": "B3LKVU05F3IDLVME",
                "key": "aYzHSI2iNhH2UyKdwjNHhAE7tasYEekhvMRBylKNmEQ="
            },
            "default": {
                "iv": "B3LKVU05F3IDLVME",
                "key": "aYzHSI2iNhH2UyKdwjNHhAE7tasYEekhvMRBylKNmEQ="
            }
        },
    },
    'amazon-fos7': {
        'user_agent': 'Mozilla/5.0 (Linux; Android 9; AFTSS Build/PS7679.4292N; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.140 Mobile Safari/537.36 All4/7.4.0-release)',
        'api_key': 'eUExTHB6dGtHZUhaRDZuU2E3QzFBQUY2dkhwelZOblU6UXFFbUVnVVVVT1hUa3piNg==',
        'client': 'amazonfire-dash',
        'platform': 'amazonfire',
        'device_model': 'AFTSS',
        'device_group': 'console',
        "keys": {
            "dash": {
                "iv": "B3LKVU05F3IDLVME",
                "key": "aYzHSI2iNhH2UyKdwjNHhAE7tasYEekhvMRBylKNmEQ="
            },
            "default": {
                "iv": "B3LKVU05F3IDLVME",
                "key": "aYzHSI2iNhH2UyKdwjNHhAE7tasYEekhvMRBylKNmEQ="
            }
        },
    },
    'amazon-fos8': {
        'user_agent': 'Mozilla/5.0 (Linux; Android 11; AFTKM Build/RS8116.2387N; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.248 Mobile Safari/537.36 All4/7.4.0-release)',
        'api_key': 'eUExTHB6dGtHZUhaRDZuU2E3QzFBQUY2dkhwelZOblU6UXFFbUVnVVVVT1hUa3piNg==',
        'client': 'amazonfire-dash',
        'device_group': 'console',
        'device_model': 'AFTKM',
        'platform': 'amazonfire',
        "keys": {
            "dash": {
                "iv": "B3LKVU05F3IDLVME",
                "key": "aYzHSI2iNhH2UyKdwjNHhAE7tasYEekhvMRBylKNmEQ="
            },
            "default": {
                "iv": "B3LKVU05F3IDLVME",
                "key": "aYzHSI2iNhH2UyKdwjNHhAE7tasYEekhvMRBylKNmEQ="
            }
        },
    },
    'freeview-hp': {
        'user_agent': 'Mozilla/5.0 (Linux ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Safari/537.36 OPR/46.0.2207.0 OMI/4.23.2.96.LIMA2.85 Model/Vestel-MB181 VSTVB MB100 FVC/8.0 (BUSH; MB181; ) HbbTV/1.6.1 (+DRM; BUSH; MB181; 3.9.5.0; ; _TV_G36_2023;) SmartTv',
        'api_key': 'Z0FJY0hFRjZZOUJ2akVMNnR4azF2TDZyQ1htQW5hZnA6MjRIYnRqSkp2SDNjTHQ4MA==',
        'client': 'fvp',
        'device_group': 'console',
        'device_model': 'mb181',
        'platform': 'freeview',
        "keys": {
            "dash": {
                "iv": "AiL6LengdaeTuz6T",
                "key": "hP8pR3Y4TYMLx2/QDlD+WRicZD1fdZNaYEgaxPF1ElQ="
            },
            "default": {
                "iv": "IHEFXHXCOINBQICX",
                "key": "xqBAWcVc2F4zVY2TJ3f9y5uNKgZD0aafkq0YHlFhxZ4="
            }
        },
    },
    'freeview-lp': {
        'user_agent': 'HbbTV/1.4.1 (+DRM; Manhattan; T3R; 0206; 1.0; com.manhattan-tv.g3; ) FVC/3.0 (Manhattan; com.manhattan-tv.g3; ) AppleWebkit/534.1 (KHTML)',
        'api_key': 'Z0FJY0hFRjZZOUJ2akVMNnR4azF2TDZyQ1htQW5hZnA6MjRIYnRqSkp2SDNjTHQ4MA==',
        'client': 'fvp',
        'device_group': 'console',
        'device_model': 't3r',
        'platform': 'freeview',
        "keys": {
            "dash": {
                "iv": "AiL6LengdaeTuz6T",
                "key": "hP8pR3Y4TYMLx2/QDlD+WRicZD1fdZNaYEgaxPF1ElQ="
            },
            "default": {
                "iv": "IHEFXHXCOINBQICX",
                "key": "xqBAWcVc2F4zVY2TJ3f9y5uNKgZD0aafkq0YHlFhxZ4="
            }
        },
    },
    'freely': {
        'user_agent': 'Mozilla/5.0 (Linux ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.128 Safari/537.36 OMI/4.24.3.93.MIKE.141 Model/Vestel-MB180 VSTVB MB100 FVC/9.0 (BUSH; MB180; ) HbbTV/1.7.1 (+DRM; BUSH; MB180; 4.26.0.0; ; _TV_G31_2024;) TiVoOS/1.0.0 (Vestel M',
        'api_key': 'Z0FJY0hFRjZZOUJ2akVMNnR4azF2TDZyQ1htQW5hZnA6MjRIYnRqSkp2SDNjTHQ4MA==',
        'client': 'fvp',
        'device_group': 'console',
        'device_model': 'mb180',
        'platform': 'freeview',
        "keys": {
            "dash": {
                "iv": "AiL6LengdaeTuz6T",
                "key": "hP8pR3Y4TYMLx2/QDlD+WRicZD1fdZNaYEgaxPF1ElQ="
            },
            "default": {
                "iv": "IHEFXHXCOINBQICX",
                "key": "xqBAWcVc2F4zVY2TJ3f9y5uNKgZD0aafkq0YHlFhxZ4="
            }
        },
    },
    'freesat': {
        'user_agent': 'Mozilla/5.0 (Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36 OPR/46.0.2207.0 OMI/4.13.6.465.Charlie.153 HbbTV/1.5.1 (+PVR+DRM; ARRIS; FS-ARS-01B; 5; ; com.arris.FS-ARS-01;) freesat/3.0 (1.5.2) Freesat_STB_BCM72604_2',
        'api_key': 'Z0FJY0hFRjZZOUJ2akVMNnR4azF2TDZyQ1htQW5hZnA6MjRIYnRqSkp2SDNjTHQ4MA==',
        'client': 'fvp',
        'device_group': 'console',
        'device_model': 'fs-ars-01b',
        'platform': 'freeview',
        "keys": {
            "dash": {
                "iv": "AiL6LengdaeTuz6T",
                "key": "hP8pR3Y4TYMLx2/QDlD+WRicZD1fdZNaYEgaxPF1ElQ="
            },
            "default": {
                "iv": "IHEFXHXCOINBQICX",
                "key": "xqBAWcVc2F4zVY2TJ3f9y5uNKgZD0aafkq0YHlFhxZ4="
            }
        },
    },
    'tizen': {
        # The web app crashes on both firefox and vivaldi.
        'user_agent': 'Mozilla/5.0 (SMART-TV; Linux; Tizen) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36 Tizen',
        'api_key': '',
        'client': '',
        'device_group': 'console',
        'device_model': '',
        'platform': '',
        "keys": {
            "dash": {
                "iv": "",
                "key": "l"
            },
            "default": {
                "iv": "",
                "key": ""
            }
        }
    },
    'soip': {
        'user_agent': 'Mozilla/5.0 (Linux; x86_64 GNU/Linux) AppleWebKit/601.1 (KHTML, like Gecko) Version/8.0 Safari/601.1 WPE Sky_OTT_RTD1319_2020/1.0.0 (Sky, XiOneUK, Wired)',
        'api_key': 'eUNFVEVrelV4ZUNzcDJvQUJJbkg5bmlPbFh6b0xtMzk6UTgxd01kSEcyNnhFTVhxNg==',
        'client': 'skyoverip',
        'device_group': 'console',
        'device_model': 'xi6',
        'platform': 'soip',
        "keys": {
            "dash": {
                "iv": "g1H0QFPJRjpOg5hM",
                "key": "tSAp4uKBFbfMs4gl"
            },
            "default": {
                "iv": "019E2jCwXpjNY7PQ",
                "key": "Q13xeiDf8e5orVWp"
            }
        },
    },
    'google': {
        'user_agent': 'Mozilla/5.0 (Linux; Android 12; Chromecast Build/STTL.240508.005; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.146 Mobile Safari/537.36 WebAppWrapper/1.0.1 (Google TV; Channel 4; google; ; )',
        'api_key': 'YUhMem5SV05MNFZkUzFzSEY1dU1XSkhrM291dEdncVI6TXFXRTdZRlFEUmV5dlpoYQ==',
        'client': 'googletv',
        'device_group': 'console',
        'device_model': 'Chromecast',
        'platform': 'google',
        "keys": {
            "dash": {
                "iv": "V9YRN3PIVXY2MHG5",
                "key": "Rm559E1lQ5DC2mbrwt8oKfU4aTW7tFYsy9xKL7YgZro="
            },
            "default": {
                "iv": "V9YRN3PIVXY2MHG5",
                "key": "Rm559E1lQ5DC2mbrwt8oKfU4aTW7tFYsy9xKL7YgZro="
            }
        },

    },
    'youview': {
        'user_agent': 'YouViewHTML/1.0 AppleWebKit/537.21 (Humax; DTRT1000; 80B07001; CDS/13.3.0; API/1.5.0; PS/1.5.0) (+DVR+FLASH+HTML+MHEG+IPCMC)',
        'api_key': 'aVlGcnlVSGJneVZYa1BqbkhwWFdqYm0wMmhnYzJhRVo6ajlwcVZZQXVGdXl2OFBhbg==',
        'client': 'yvdash',
        'device_group': 'console',
        'device_model': 'dtrt1000',
        'platform': 'youview',
        "keys": {
            "dash": {
                "iv": "OEEHpIWo1Ui08PUy",
                "key": "OB+18N8fmMy+/keHOt4gwoy2WTRg1o7jwHLKPXmIf2s="
            },
            "default": {
                "iv": "x6n8h7QSflulsoIc",
                "key": "o9HEUry37U5haDIuIsXGkxqyR3VBkQhD"
            }
        },
    },
    'youview-2020': {
        'user_agent': 'Mozilla/5.0 (Linux; Andr0id 9; BRAVIA 4K UR3 Build/PTT1.190515.001.S42) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36 OPR/46.0.2207.0 OMI/4.13.5.431.DIA5HBBTV.143 HbbTV/1.5.1 (+DRM; Sony; 43NB---QBS4; PKG6.4624.0605EUA; ; com.sony.HE.G3.4K; ) sony.hbbtv.tv.G3.2020HE.4K YouView',
        'api_key': 'aVlGcnlVSGJneVZYa1BqbkhwWFdqYm0wMmhnYzJhRVo6ajlwcVZZQXVGdXl2OFBhbg==',
        'client': 'yvdash',
        'device_group': 'console',
        'device_model': '43nb---qbs4',
        'platform': 'youview',
        "keys": {
            "dash": {
                "iv": "OEEHpIWo1Ui08PUy",
                "key": "OB+18N8fmMy+/keHOt4gwoy2WTRg1o7jwHLKPXmIf2s="
            },
            "default": {
                "iv": "x6n8h7QSflulsoIc",
                "key": "o9HEUry37U5haDIuIsXGkxqyR3VBkQhD"
            }
        },
    },
    'ps4': {
        'user_agent': 'Mozilla/5.0 (PlayStation 4) AppleWebKit/531.3 (KHTML, like Gecko) SCEE/1.0 Nuanti/2.0',
        'api_key': 'b2NrNXdORGJhVVhsZFhrNTIxZVFJNldobVVUS2MxYjk6ajQ2WFJkN0cxTWozNnRKSQ==',
        'client': 'ps-dash',
        'device_group': 'console',
        'device_model': 'PlayStation 4',
        'platform': 'ps4',
        "keys": {
            "dash": {
                "iv": "IHEFXHXCOINBQICX",
                "key": "xqBAWcVc2F4zVY2TJ3f9y5uNKgZD0aafkq0YHlFhxZ4="
            },
            "default": {
                "iv": "IHEFXHXCOINBQICX",
                "key": "xqBAWcVc2F4zVY2TJ3f9y5uNKgZD0aafkq0YHlFhxZ4="
            }
        },
    },
    'ps5': {
        'user_agent': 'Mozilla/5.0 (PlayStation; PlayStation 5/7.61) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
        'api_key': 'b2NrNXdORGJhVVhsZFhrNTIxZVFJNldobVVUS2MxYjk6ajQ2WFJkN0cxTWozNnRKSQ==',
        'client': 'ps-dash',
        'device_group': 'console',
        'device_model': 'PlayStation 5',
        'platform': 'ps4',
        "keys": {
            "dash": {
                "iv": "IHEFXHXCOINBQICX",
                "key": "xqBAWcVc2F4zVY2TJ3f9y5uNKgZD0aafkq0YHlFhxZ4="
            },
            "default": {
                "iv": "IHEFXHXCOINBQICX",
                "key": "xqBAWcVc2F4zVY2TJ3f9y5uNKgZD0aafkq0YHlFhxZ4="
            }
        },
    },
    'virgin': {
        'user_agent': 'Mozilla/5.0 (Linux armv7l) AppleWebKit/602.1.28+ (KHTML, like Gecko) Version/9.1 Safari/601.5.17, VirginMedia_STB_05.4525.9616.13/EOS1008C-mon-web-00.01-070-ac-AL-20190509163540-un000 (Humax_liberty,EOS-1008C,Wired) HZN/4.18',
        'api_key': 'SlZ3eUxiaFFidFFTMXAwWmRSSmJUOWJubERsZTJ0QnU6Y0hQU2pDNHpIcjRLY3MwVg==',
        'client': 'virginall4',
        'device_group': 'console',
        'device_model': 'EOS-1008C',
        'platform': 'tivo',
        "keys": {
            "dash": {
                "iv": "019E2jCwXpjNY7PQ",
                "key": "Q13xeiDf8e5orVWp"
            },
            "default": {
                "iv": "019E2jCwXpjNY7PQ",
                "key": "Q13xeiDf8e5orVWp"
            }
        },
    },
    'tivo': {
        'user_agent': 'Mozilla/5.0 (Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36 OPR/36.0.2128.0 OMI/4.8.0.129.JFK.695 TiVo, VirginMedia_STB_BCM7252s/20.12.1.RC12-VMB-11 (VirginMedia, TCDC68000, Wired) - Google Inc.',
        'api_key': 'SlZ3eUxiaFFidFFTMXAwWmRSSmJUOWJubERsZTJ0QnU6Y0hQU2pDNHpIcjRLY3MwVg==',
        'client': 'virginall4',
        'device_group': 'console',
        'device_model': 'TCDC68000,',   # Yes, including the comma!
        'platform': 'tivo',
        "keys": {
            "dash": {
                "iv": "019E2jCwXpjNY7PQ",
                "key": "Q13xeiDf8e5orVWp"
            },
            "default": {
                "iv": "019E2jCwXpjNY7PQ",
                "key": "Q13xeiDf8e5orVWp"
            }
        },
    },
    'skyq': {
        'user_agent': 'Mozilla/5.0 (X11; Linux armv71) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.9.7 Chrome/56.0.2924122 Safari/537.36 Sky_STB ST412 2018/1.0.0 (Sky, ES130UK)',
        'api_key': 'eUNFVEVrelV4ZUNzcDJvQUJJbkg5bmlPbFh6b0xtMzk6UTgxd01kSEcyNnhFTVhxNg==',
        'client': 'skyoverip',
        'device_group': 'console',
        'device_model': 'xi6',
        'platform': 'soip',
        "keys": {
            "dash": {
                "iv": "g1H0QFPJRjpOg5hM",
                "key": "tSAp4uKBFbfMs4gl"
            },
            "default": {
                "iv": "019E2jCwXpjNY7PQ",
                "key": "Q13xeiDf8e5orVWp"
            }
        },
    },
    'xbox': {
        # Web app crashes with error: "Failed to load platform package" on google.bsd.client.. and freeview.bsd.client..
        # 503 error on xbox.bsd.client...
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox One; MSAppHost/3.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.26100',
        'api_key': '',
        'client': '',
        'device_group': 'console',
        'device_model': '',
        'platform': '',
        "keys": {
            "dash": {
                "iv": "",
                "key": ""
            },
            "default": {
                "iv": "",
                "key": ""
            }
        },
    },
}
