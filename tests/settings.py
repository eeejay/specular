configs = {
    'windows' : {
            'host' : '11.0.0.2',
            'browsers' : {
                        'firefox3' : '*chrome',
                        'safari' : '*safari C:\Documents and Settings\Eitan\Desktop\webkit-nightly\Safari.exe'
                        }
            },
    'linux' : {
            'host' : 'localhost',
            'browsers' : {
                        'firefox3' : '*chrome /usr/lib/firefox-3.0.2/firefox',
                        'midori' : '*custom /usr/bin/midori',
                        'epiphany' : '*custom /usr/bin/epiphany'
                        }
            }
    }

current_host = None
current_command = None
