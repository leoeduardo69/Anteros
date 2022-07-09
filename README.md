# ANTEROS APP
#### Video Demo:  <https://youtu.be/yDKYoMZZ4xo>
#### Description:

I would like to introduce the Anteros App, a tool created to show correlation between financial instruments in a graphical way and as intuitive as possible.

The correlation value is display as matrix shape. There are two different periods displayed above and below the diagonal. Here the intensity of the colour is also related to the magnitude of the correlation.

This app is created because there is a lack of a functionality like this in any trading software.

Let’s talk in deep about this app.

Anteros? Why does this app is called like this? In greek mythology Anteros was the god of requited love and also the punisher of those who scorn love. So “love” in this context is an analogy of how financial instruments are correlated between others or a lack of correlation at all.

When the app is launched a “welcome window” is displayed, here you choose all the settings for run the programme.

For use the app, you need an API key for downloading the financial data. By clicking on “Get an API KEY for downloading live data”, you will be directed to the web page of “Alpha Vantage”. This provider is chosen because it provides live data for free and you only need an email for get an Api Key.

Once you get the key, copy paste it in API KEY place.

In order to calculate a correlation between two financial markets, you need to specify how many points in the past you are analysing. In other words, what are the periods in which you want to implement the correlation analysis.


You also need to provide a timeframe in which you are trading. It can be 5, 15, 30 or 60 minutes intervals.

Of course, you also provide the correlation type. Pearson or Spearman type. “Pearson” is the one I am sure you know about. It measures how two instruments depend on each other in a linear way. Spearman correlation is basically the same but it takes in account non linear relations.

Some people believe that Spearman correlation is more suitable for technical analysis. That’s why that option is here.

Finally you need to choose the financial instruments you want to analyse. At the moment, there is only one type of financial instruments to choose: the forex market. In a future version of the Anteros App will support many other types of assets.

As you can imagine, you need to choose minimum two pairs of currencies and a maximum of five pairs. Five instruments per minute is the limit that establish “Alpha Vantage” for download data for free.

Next time you launch the app, all your settings are saved, so you do not need to configure the app every time you started.

Finally you click on “Launch” for starting the app.

After the lunching, you wait some seconds until the connection with the provider is stablished and some data is downloaded.



The main window consist of a matrix where the names of the instruments are displayed in every side.

The cross between elements is the value of correlation at this moment.

In the diagonal, you see a reminder of the period you are analysing. Values above the diagonals are the values corresponding to that specific period of time and equivalent for values below the diagonal.

You can resize that window as you will.

The colours of the value frames are according to the correlation, values near minus one are displayed in pink, values near one are displayed in blue and values near cero are displayed in grey. The colour intensity also provides a visual reference for correlation values.

When you click on a correlation value, a candle chart is open for both instruments and a chart of correlation evolution across the time.

On top of the graphic is the instant of close for the last candle. It means the correlation is calculated based on the last bar fully closed.

The app doesn’t provide “real time data” because it is calculated when the last bar or period of time is fully closed. So, it is almost real time data

There are also some labels located at the period-length of the graphic for an easy interpretation of the period of analysis for the correlation.

Is good to said at this point, that the correlation value is calculated on “close price”.

The graphic is not a picture, you can resize it, zoom on it, navigate on it and save a picture of it as well.

When the currently bar will be closed then correlation values are updated.

Well… that’s it! The Anteros app for display, in useful way, the correlation between financial instruments.

I hope you like it and I hope it is useful for your trading and your investment analysis.
