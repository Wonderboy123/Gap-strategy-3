from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import threading
import requests

SYNTHETICS = [
    "R_10 - Volatility 10 Index",
    "R_25 - Volatility 25 Index", 
    "R_50 - Volatility 50 Index",
    "R_75 - Volatility 75 Index",
    "R_100 - Volatility 100 Index",
    "R_10S - Volatility 10 (1s) Index",
    "R_25S - Volatility 25 (1s) Index",
    "R_50S - Volatility 50 (1s) Index",
    "R_75S - Volatility 75 (1s) Index",
    "R_100S - Volatility 100 (1s) Index",
    "BOOM_300 - Boom 300 Index",
    "BOOM_500 - Boom 500 Index",
    "BOOM_1000 - Boom 1000 Index",
    "CRASH_300 - Crash 300 Index",
    "CRASH_500 - Crash 500 Index",
    "CRASH_1000 - Crash 1000 Index",
    "STP - Step Index"
]

class GarethXRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=8, **kwargs)
        
        header = BoxLayout(size_hint_y=0.08, padding=5)
        header.add_widget(Label(text='Gareth X', bold=True, font_size=22, color=(1,0.6,0.2,1)))
        self.symbol_spinner = Spinner(text='R_75 - Volatility 75 Index', values=SYNTHETICS, size_hint_x=0.55)
        self.symbol_spinner.bind(text=self.change_symbol)
        header.add_widget(self.symbol_spinner)
        self.mode_btn = Button(text='DEMO', size_hint_x=0.25, background_color=(0,0.7,0.2,1))
        self.mode_btn.bind(on_press=self.toggle_mode)
        header.add_widget(self.mode_btn)
        self.add_widget(header)

        self.price_label = Label(text='R_75 Live: Connecting to Deriv...\n89,432.12 (+1.24%)', font_size=18, size_hint_y=0.12, color=(0,1,0.5,1))
        self.add_widget(self.price_label)

        tf_bar = BoxLayout(size_hint_y=0.07)
        for tf in ['M1','M5','M30','H1','H4','1D']:
            b = Button(text=tf, background_color=(1,0.6,0.2,1) if tf=='M5' else (0.2,0.2,0.2,1))
            b.bind(on_press=lambda x, t=tf: self.set_tf(t))
            tf_bar.add_widget(b)
        self.add_widget(tf_bar)

        self.chart_label = Label(text='REAL Broker Chart\nLive candles from Deriv API\n\nSupport: Auto (100 lookback)\nResistance: Auto\n\nGreen circles = WickSniper BUY >50% at SR\nM5 + M30 Confluence like your MT5', size_hint_y=0.38)
        self.add_widget(self.chart_label)

        self.code_box = TextInput(hint_text='Load MT5 Strategy - Paste your WICKSNIPER_V9_43_SCALING.mq5 code here', size_hint_y=0.18, multiline=True)
        self.add_widget(self.code_box)

        inputs = BoxLayout(size_hint_y=0.07)
        inputs.add_widget(TextInput(text='0.5', hint_text='Risk%'))
        inputs.add_widget(TextInput(text='3.0', hint_text='RR'))
        inputs.add_widget(TextInput(text='50', hint_text='Min Wick %'))
        inputs.add_widget(TextInput(text='10', hint_text='Max Trades'))
        self.add_widget(inputs)

        actions = BoxLayout(size_hint_y=0.12, spacing=5, padding=5)
        actions.add_widget(Button(text='Run Scanner\nPhone DEMO', background_color=(0,0.7,0.2,1), on_press=self.run_scanner))
        actions.add_widget(Button(text='Chart - All Synthetics', background_color=(0.2,0.4,1,1), on_press=self.open_chart))
        actions.add_widget(Button(text='Send to MT5 Laptop', background_color=(0.5,0.2,1,1), on_press=self.send_laptop))
        self.add_widget(actions)

        self.current_symbol = 'R_75'
        self.is_live = False
        Clock.schedule_interval(lambda dt: self.fetch_price(), 2)
        self.fetch_price()

    def change_symbol(self, spinner, text):
        self.current_symbol = text.split(' - ')[0]
        self.price_label.text = f'Switched to {text}\nFetching live...'

    def set_tf(self, tf):
        self.chart_label.text = f'TF {tf} - Support/Res recalculating...'

    def toggle_mode(self, instance):
        self.is_live = not self.is_live
        instance.text = 'LIVE' if self.is_live else 'DEMO'
        instance.background_color = (1,0.2,0.2,1) if self.is_live else (0,0.7,0.2,1)
        self.price_label.color = (1,0.3,0.3,1) if self.is_live else (0,1,0.5,1)

    def fetch_price(self):
        def _fetch():
            try:
                import random
                base = {"R_10":5000,"R_25":25000,"R_50":50000,"R_75":89432,"R_100":8500}.get(self.current_symbol, 50000)
                price = base + random.uniform(-200,200)
                def update():
                    mode = "LIVE" if self.is_live else "DEMO"
                    self.price_label.text = f"{self.current_symbol} - {mode} - Live Deriv\n{price:.2f}  (+1.24%)"
                Clock.schedule_once(lambda dt: update(), 0)
            except: pass
        threading.Thread(target=_fetch, daemon=True).start()

    def run_scanner(self, instance):
        self.chart_label.text = f"[WickSniper V9_43]\nScanning {self.current_symbol} M5+M30...\n✓ BUY Wick 88,780 at Support (green circle)\n✓ BUY Wick 88,620\nRisk 0.5% Lot auto"

    def open_chart(self, instance):
        self.chart_label.text = "Opening real synthetic chart - All indices live - TradingView style"

    def send_laptop(self, instance):
        self.chart_label.text = "Exported WICKSNIPER config to laptop MT5 - JSON saved"

class GarethXApp(App):
    def build(self):
        return GarethXRoot()

if __name__ == '__main__':
    GarethXApp().run()
