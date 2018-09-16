import parser42
import webbrowser

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label


import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_finance import candlestick_ohlc
from matplotlib.dates import MONDAY, DateFormatter, WeekdayLocator


class DummyApp(App):

    def build_config(self, config):
        config.setdefaults('main_manu', {
            'limit_currincies': 20,
        })

    def build(self):
        root = BoxLayout(orientation='horizontal', padding=3)

        # left crypto currency menu
        left_bar = ScrollView(size_hint=[.4, 1])
        left_grid = GridLayout(cols=1, size_hint_y=2)
        left_grid.bind(minimum_height=left_grid.setter('height'))

        config = self.config
        limit_currincies = int(config.get('main_manu', 'limit_currincies'))

        currencies = parser42.top_currincies(limit_currincies)
        for index in range(limit_currincies):
            currency = next(currencies)
            left_grid.add_widget(Button(
                text=currency[0],
                on_press=self.update_scree,
                background_color=(0, 0, 0, 1)))

        left_bar.add_widget(left_grid)

        # info head
        self.tittle = Label(text='BTC')
        self.price = Label(text='7453.459')
        self.changes = Label(text='1h: 0.3 24h: -2.1 7d: 34.23')

        inform_bar = BoxLayout(orientation='horizontal', size_hint_y=None)
        inform_bar.add_widget(self.tittle)
        inform_bar.add_widget(self.price)
        inform_bar.add_widget(self.changes)

        # graph

        self.graph = BoxLayout()
        self.graph.add_widget(self.get_graph('BTC'))
        # news
        self.news = GridLayout(cols=1, size_hint_y=1.6, padding=3)
        self.news.bind(minimum_height=self.news.setter('height'))
        self.main_news('bitcoin')
        scrol_news = ScrollView(size_hint=[1, 1])
        scrol_news.add_widget(self.news)

        right_bar = BoxLayout(orientation='vertical', padding=3)
        right_bar.add_widget(inform_bar)
        right_bar.add_widget(self.graph)
        right_bar.add_widget(scrol_news)

        root.add_widget(left_bar)
        root.add_widget(right_bar)

        return root

    def update_scree(self, instance):
        data = parser42.get_currency(instance.text)
        self.tittle.text = data[6]
        self.price.text = str(data[1])
        self.changes.text = '1h: {} 24h: {} 7d: {}'.format(
            data[2], data[4], data[5])
        self.main_news(data[6])
        self.graph.clear_widgets()
        self.graph.add_widget(self.get_graph(data[0]))

    def main_news(self, crypto):
        self.news.clear_widgets()
        ref = lambda instance, url: webbrowser.open_new(url)
        for article in parser42.get_news(crypto):
            boxlayout = BoxLayout(orientation='vertical', padding=3)
            text = ('[ref={}]'.format(article['url']) +
                    '[b]' +
                    article['title'] +
                    '[/b]' +
                    '\n' +
                    article['description'] +
                    '\n' +
                    article['publishedAt'][:10] +
                    '[/ref]')
            completed_article = Label(text=text,
                                      markup=True,
                                      text_size=[800, 100],
                                      on_ref_press=ref,
                                      )
            boxlayout.add_widget(completed_article)
            self.news.add_widget(boxlayout)

    def get_graph(self, crypto):
        plt.clf()
        fig, ax = plt.subplots(figsize=(10, 5), dpi=400,
                               facecolor='black')
        ax.set_facecolor('black')
        fig.subplots_adjust(left=0.01, top=1.00, right=1.00, bottom=0.01)
        self.graph_data = parser42.get_histodata(crypto)
        candlestick_ohlc(ax, self.graph_data, colorup='g')
        return FigureCanvas(fig)



if __name__ == '__main__':
    DummyApp().run()
