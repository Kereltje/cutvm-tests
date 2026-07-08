var availableUserAgents = {
    "amazon-fos5": "Mozilla/5.0 (Linux; Android 5.1.1; AFTT Build/LVY48F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.220 Mobile Safari/537.36 All4/7.4.0-release)",
    "amazon-fos6": "Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6705; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/118.0.0.0 Mobile Safari/537.36 All4/7.4.0-release)",
    "amazon-fos7": "Mozilla/5.0 (Linux; Android 9; AFTSS Build/PS7679.4292N; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.140 Mobile Safari/537.36 All4/7.4.0-release)",
    "amazon-fos8": "Mozilla/5.0 (Linux; Android 11; AFTKM Build/RS8116.2387N; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.248 Mobile Safari/537.36 All4/7.4.0-release)",
    "freeview-hp": "Mozilla/5.0 (Linux ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Safari/537.36 OPR/46.0.2207.0 OMI/4.23.2.96.LIMA2.85 Model/Vestel-MB181 VSTVB MB100 FVC/8.0 (BUSH; MB181; ) HbbTV/1.6.1 (+DRM; BUSH; MB181; 3.9.5.0; ; _TV_G36_2023;) SmartTv",
    "freeview-lp": "HbbTV/1.4.1 (+DRM; Manhattan; T3R; 0206; 1.0; com.manhattan-tv.g3; ) FVC/3.0 (Manhattan; com.manhattan-tv.g3; ) AppleWebkit/534.1 (KHTML)",
    "freely": "Mozilla/5.0 (Linux ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.128 Safari/537.36 OMI/4.24.3.93.MIKE.141 Model/Vestel-MB180 VSTVB MB100 FVC/9.0 (BUSH; MB180; ) HbbTV/1.7.1 (+DRM; BUSH; MB180; 4.26.0.0; ; _TV_G31_2024;) TiVoOS/1.0.0 (Vestel M",
    "freesat": "Mozilla/5.0 (Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36 OPR/46.0.2207.0 OMI/4.13.6.465.Charlie.153 HbbTV/1.5.1 (+PVR+DRM; ARRIS; FS-ARS-01B; 5; ; com.arris.FS-ARS-01;) freesat/3.0 (1.5.2) Freesat_STB_BCM72604_2",
    "tizen": "Mozilla/5.0 (SMART-TV; Linux; Tizen) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36 Tizen",
    "soip": "Mozilla/5.0 (Linux; x86_64 GNU/Linux) AppleWebKit/601.1 (KHTML, like Gecko) Version/8.0 Safari/601.1 WPE Sky_OTT_RTD1319_2020/1.0.0 (Sky, XiOneUK, Wired)",
    "google": "Mozilla/5.0 (Linux; Android 12; Chromecast Build/STTL.240508.005; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.146 Mobile Safari/537.36 WebAppWrapper/1.0.1 (Google TV; Channel 4; google; ; )",
    "youview": "YouViewHTML/1.0 AppleWebKit/537.21 (Humax; DTRT1000; 80B07001; CDS/13.3.0; API/1.5.0; PS/1.5.0) (+DVR+FLASH+HTML+MHEG+IPCMC)",
    "youview-2020": "Mozilla/5.0 (Linux; Andr0id 9; BRAVIA 4K UR3 Build/PTT1.190515.001.S42) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36 OPR/46.0.2207.0 OMI/4.13.5.431.DIA5HBBTV.143 HbbTV/1.5.1 (+DRM; Sony; 43NB---QBS4; PKG6.4624.0605EUA; ; com.sony.HE.G3.4K; ) sony.hbbtv.tv.G3.2020HE.4K YouView",
    "ps4": "Mozilla/5.0 (PlayStation 4) AppleWebKit/531.3 (KHTML, like Gecko) SCEE/1.0 Nuanti/2.0",
    "ps5": "Mozilla/5.0 (PlayStation; PlayStation 5/7.61) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    "virgin": "Mozilla/5.0 (Linux armv7l) AppleWebKit/602.1.28+ (KHTML, like Gecko) Version/9.1 Safari/601.5.17, VirginMedia_STB_05.4525.9616.13/EOS1008C-mon-web-00.01-070-ac-AL-20190509163540-un000 (Humax_liberty,EOS-1008C,Wired) HZN/4.18",
    "tivo": "Mozilla/5.0 (Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36 OPR/36.0.2128.0 OMI/4.8.0.129.JFK.695 TiVo, VirginMedia_STB_BCM7252s/20.12.1.RC12-VMB-11 (VirginMedia, TCDC68000, Wired) - Google Inc.",
    "skyq": "Mozilla/5.0 (X11; Linux armv71) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.9.7 Chrome/56.0.2924122 Safari/537.36 Sky_STB ST412 2018/1.0.0 (Sky, ES130UK)",
    "xbox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox One; MSAppHost/3.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.26100"
};

function getQueryParam(param) {
    var urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

function forceChangeUserAgent(window, userAgent) {
    if (navigator.__defineGetter__) {
        navigator.__defineGetter__('userAgent', function () {
            return userAgent;
        });
    } else if (Object.defineProperty) {
        Object.defineProperty(navigator, 'userAgent', {
            get: function () {
                return userAgent;
            }
        });
    }
    if (window.navigator.userAgent !== userAgent) {
        var userAgentProp = {
            get: function () {
                return userAgent;
            }
        };
        try {
            Object.defineProperty(window.navigator, 'userAgent', userAgentProp);
        } catch (e) {
            window.navigator = Object.create(navigator, {
                userAgent: userAgentProp
            });
        }
    }
}

(() => {
    var deviceToEmulate = getQueryParam('device');
    if (!deviceToEmulate || !availableUserAgents[deviceToEmulate]) {
        console.warn(`Using default user agent: "${window.navigator.userAgent}"`);
        return;
    }
    console.log(`Emulating device ${deviceToEmulate}`);
    var emulatedUserAgent = availableUserAgents[deviceToEmulate];
    forceChangeUserAgent(window, emulatedUserAgent);
    console.log(`Switching user agent to "${window.navigator.userAgent}"`);
})();
