import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as font
import os
import json
import time
import multiprocessing
import pandas as pd
import datetime #the moment now
import requests
import mplfinance as mpf
import io
from numpy.lib.stride_tricks import as_strided
from numpy.lib import pad
import numpy as np
from functools import partial
# API_KEY = '8ZMOE8BJMGDVP1PU' # or 'fdsfdfdsf' 

#TODO: check times and call the API, and check the time waits periods, check NaN values

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/' # For saving downloaded data

    # starting main loop tk  
    root = tk.Tk()
    # set background color of the window

    ''' ----------   LOGIN WINDOW ---------- '''
    loginWindow = tk.Toplevel (root) # create a new window
    loginWindow.title('CORRELATION SET UP')
    loginWindow.configure(background = "white") # set background color of login/setup window

    # Read and save settings in login window and check if they are valid
    def get_configuration(loginAndConfiguration, list_instruments):
        """ Extract the configuration from the login window and check if it is valid """
        # Get the API key
        loginAndConfiguration["API_KEY"] = apikey.get()
        # Get timeframe and check if it is valid
        if resolution.get() in ['5min', '15min', '30min', '60min']:
            loginAndConfiguration["RESOLUTION"] = resolution.get()
        else:
            messagebox.showwarning(title='Error with Anteros Settings', message='resolution not valid')
            return
        # Get the correlation periods and check if they are valid
        try:
            loginAndConfiguration["CORRELATION_PERIODS_1"] = int(corrper1.get())
            loginAndConfiguration["CORRELATION_PERIODS_2"] = int(corrper2.get())
        except:
            messagebox.showwarning(title='Error with Anteros Settings', message='Correlation period should be a interger number')
            return
        # Get the correlation type and check if it is valid
        if correlationType.get() in ('pearson', 'spearman'):
            loginAndConfiguration["CORRELATION_TYPE"] = correlationType.get()
        else:
            messagebox.showwarning(title='Error with Anteros Settings', message='Select a valid correlation type')
            return
        # Get the instruments and check if they are valid
        if instrument1.get() in list_instruments[1:] and instrument2.get() in list_instruments[1:]: #first instrument is "none"
            loginAndConfiguration["INSTRUMENTS_1"] = instrument1.get()
            loginAndConfiguration["INSTRUMENTS_2"] = instrument2.get()
            loginAndConfiguration["INSTRUMENTS_3"] = instrument3.get()
            loginAndConfiguration["INSTRUMENTS_4"] = instrument4.get()
            loginAndConfiguration["INSTRUMENTS_5"] = instrument5.get()
        else:
            messagebox.showwarning(title='Error with Anteros Settings', message='Select at least the first two valid instruments')
            return
        if instrument3.get() in list_instruments and instrument4.get() in list_instruments and instrument5.get() in list_instruments:
            loginAndConfiguration["INSTRUMENTS_3"] = instrument3.get()
            loginAndConfiguration["INSTRUMENTS_4"] = instrument4.get()
            loginAndConfiguration["INSTRUMENTS_5"] = instrument5.get()
        else:
            messagebox.showwarning(title='Error with Anteros Settings', message='instrument not valid')
            return
        # Open a file and save the Anteros Settings for future use
        with open(dir_path + 'ANTEROS_CONFIGURATION'+'.json', 'w') as dummy_json:
            loginAndConfiguration=json.dump(loginAndConfiguration, dummy_json)
        loginWindow.quit()
        loginWindow.destroy()
        loginWindow.update()
        return

    # Read if there are login settings
    try: 
        with open(dir_path + 'ANTEROS_CONFIGURATION'+'.json', 'r') as dummy_json:
            loginAndConfiguration=json.load(dummy_json)
    except: # Create a dictionary with intial values
        loginAndConfiguration = {}
        loginAndConfiguration["API_KEY"] = ""
        loginAndConfiguration["RESOLUTION"] = ""
        loginAndConfiguration["CORRELATION_PERIODS_1"] = ""
        loginAndConfiguration["CORRELATION_PERIODS_2"] = ""
        loginAndConfiguration["CORRELATION_TYPE"] = ""
        loginAndConfiguration["INSTRUMENTS_1"] = "please select"
        loginAndConfiguration["INSTRUMENTS_2"] = "please select"
        loginAndConfiguration["INSTRUMENTS_3"] = "none"
        loginAndConfiguration["INSTRUMENTS_4"] = "none"
        loginAndConfiguration["INSTRUMENTS_5"] = "none"
    
    # Welcome message
    tk.Label(loginWindow ,text = "WELCOME TO ANTEROS APP",bg="white",fg="maroon").grid(row = 7,column = 0, columnspan= 2)
    tk.Label(loginWindow ,text = "a software for display correlation between finantial instruments",bg="white",fg="maroon").grid(row = 8,column = 0, columnspan= 2)


    # API KEY
    tk.Label(loginWindow ,text = "API KEY",bg="white",fg="maroon").grid(row = 10,column = 0)
    apikey = tk.StringVar(loginWindow, value=loginAndConfiguration["API_KEY"])
    api_key_input = tk.Entry(loginWindow,textvariable=apikey, bg="white",fg="black").grid(row = 10,column = 1)

    # CORRELATION 1
    tk.Label(loginWindow ,text = "CORRELATION PERIOD 1",bg="white",fg="maroon").grid(row = 11,column = 0)
    corrper1 = tk.StringVar(loginWindow, value=loginAndConfiguration["CORRELATION_PERIODS_1"])
    corre_periods_input = tk.Entry(loginWindow,textvariable=corrper1,bg="white",fg="black").grid(row = 11,column = 1)

    # CORRELATION 2
    tk.Label(loginWindow ,text = "CORRELATION PERIOD 2",bg="white",fg="maroon").grid(row = 12,column = 0)
    corrper2 = tk.StringVar(loginWindow, value=loginAndConfiguration["CORRELATION_PERIODS_2"])
    corre_periods_input = tk.Entry(loginWindow,textvariable=corrper2,bg="white",fg="black").grid(row = 12,column = 1)

    # RESOLUTION
    tk.Label(loginWindow ,text = "RESOLUTION",bg="white",fg="maroon").grid(row = 13,column = 0)
    s = ttk.Style().configure('TCombobox', bg='white', fg='black')
    resol = tk.StringVar(loginWindow, value=loginAndConfiguration["RESOLUTION"])
    resolution = ttk.Combobox(loginWindow, textvariable = resol, justify='center', style='TCombobox')
    resolution['values'] = (loginAndConfiguration["RESOLUTION"], '5min', '15min', '30min', '60min' )
    resolution.grid(row = 13,column = 1)

    # CORRELATION TYPE
    tk.Label(loginWindow ,text = "CORRELATION TYPE",bg="white",fg="maroon").grid(row = 14,column = 0)
    corrtyp = tk.StringVar(loginWindow, value=loginAndConfiguration["CORRELATION_TYPE"])
    correlationType = ttk.Combobox(loginWindow, textvariable = corrtyp, justify='center', style='TCombobox')
    correlationType['values'] = (loginAndConfiguration["CORRELATION_TYPE"], 'pearson', 'spearman')
    correlationType.grid(row = 14,column = 1)

    # INSTRUMENTS
    list_instruments = ("none", 'AUDJPY','AUDUSD', 'USDJPY' ,'EURAUD', 'EURJPY', 'EURUSD',  'USDCHF', 'EURCHF','AUDCHF','CHFJPY','AUDNZD','NZDUSD','NOKSEK','NOKJPY','SEKJPY','EURNOK','EURSEK', 'EURGBP', 'GBPUSD', 'GBPJPY', 'AUDGBP', 'EURCAD', 'USDCAD')
    
    # INTRUMENT 1
    tk.Label(loginWindow ,text = "INSTRUMENT 1",bg="white",fg="maroon").grid(row = 15,column = 0)
    instr1 = tk.StringVar(loginWindow, value=loginAndConfiguration["INSTRUMENTS_1"])
    instrument1 = ttk.Combobox(loginWindow, textvariable = instr1, justify='center', style='TCombobox')
    instrument1['values'] = ( loginAndConfiguration["INSTRUMENTS_1"], ) + list_instruments 
    instrument1.grid(row = 15,column = 1)

    # INTRUMENT 2
    tk.Label(loginWindow ,text = "INSTRUMENT 2",bg="white",fg="maroon").grid(row = 16,column = 0)
    instr2 = tk.StringVar(loginWindow, value=loginAndConfiguration["INSTRUMENTS_2"])
    instrument2 = ttk.Combobox(loginWindow, textvariable = instr2, justify='center', style='TCombobox')
    instrument2['values'] = ( loginAndConfiguration["INSTRUMENTS_2"], ) + list_instruments 
    instrument2.grid(row = 16,column = 1)

    # INTRUMENT 3
    tk.Label(loginWindow ,text = "INSTRUMENT 3",bg="white",fg="maroon").grid(row = 17,column = 0)
    instr3 = tk.StringVar(loginWindow, value=loginAndConfiguration["INSTRUMENTS_3"])
    instrument3 = ttk.Combobox(loginWindow, textvariable = instr3, justify='center', style='TCombobox')
    instrument3['values'] = ( loginAndConfiguration["INSTRUMENTS_3"], ) + list_instruments 
    instrument3.grid(row = 17,column = 1)

    # INTRUMENT 4
    tk.Label(loginWindow ,text = "INSTRUMENT 4",bg="white",fg="maroon").grid(row = 18,column = 0)
    instr4 = tk.StringVar(loginWindow, value=loginAndConfiguration["INSTRUMENTS_4"])
    instrument4 = ttk.Combobox(loginWindow, textvariable = instr4, justify='center', style='TCombobox')
    instrument4['values'] = ( loginAndConfiguration["INSTRUMENTS_4"], ) + list_instruments 
    instrument4.grid(row = 18,column = 1)

    # INTRUMENT 5
    tk.Label(loginWindow ,text = "INSTRUMENT 5",bg="white",fg="maroon").grid(row = 19,column = 0)
    instr5 = tk.StringVar(loginWindow, value=loginAndConfiguration["INSTRUMENTS_5"])
    instrument5 = ttk.Combobox(loginWindow, textvariable = instr5, justify='center', style='TCombobox')
    instrument5['values'] = ( loginAndConfiguration["INSTRUMENTS_5"], ) + list_instruments 
    instrument5.grid(row = 19,column = 1)

    # Login Button
    launch = tk.Button(loginWindow, text="Launch Anteros", fg="Black", highlightbackground="white", padx=50, pady=10, borderwidth=5,  height = 1, width = 1 , command=partial(get_configuration,loginAndConfiguration, list_instruments))
    launch.grid(row=30, column=0, columnspan= 2)

    # Hyperlink button
    import webbrowser
    def callback():
        webbrowser.open_new("https://www.alphavantage.co/support/")
    get_api_link= tk.Button(loginWindow, text="Get an API KEY for download live data", command=callback,  fg="Black", highlightbackground="white", padx=150, pady=5, borderwidth=5,  height = 1, width = 1)
    get_api_link.grid(row=9, column=0, columnspan= 2)
    

    
    # Wait until first level window is closed
    root.wait_window(loginWindow)

    ''' ---------- SETUP VALUES ---------- '''
    # Extracting configuration for connecting to API
    API_KEY = loginAndConfiguration["API_KEY"]
    RESOLUTION = loginAndConfiguration["RESOLUTION"]
    CORRELATION_PERIODS = [loginAndConfiguration["CORRELATION_PERIODS_1"], loginAndConfiguration["CORRELATION_PERIODS_2"]]
    CORRELATION_TYPE = loginAndConfiguration["CORRELATION_TYPE"] # 'pearson' or 'spearman'
    INSTRUMENTS_NAMES = [loginAndConfiguration["INSTRUMENTS_1"], loginAndConfiguration["INSTRUMENTS_2"]]
    if loginAndConfiguration["INSTRUMENTS_3"] != 'none':
        INSTRUMENTS_NAMES.append(loginAndConfiguration["INSTRUMENTS_3"])
    if loginAndConfiguration["INSTRUMENTS_4"] != 'none':
        INSTRUMENTS_NAMES.append(loginAndConfiguration["INSTRUMENTS_4"])
    if loginAndConfiguration["INSTRUMENTS_5"] != 'none':
        INSTRUMENTS_NAMES.append(loginAndConfiguration["INSTRUMENTS_5"])
    
    if RESOLUTION=='5min':
        time_frame=5
    elif RESOLUTION=='15min' :
        time_frame=15
    elif RESOLUTION=='30min' :
        time_frame=30
    elif RESOLUTION=='60min': 
        time_frame=60

    # Saving instruments for call the data provider
    # ONLY for forex data
    INSTRUMENTS = [] # for download API
    for instrument_name in INSTRUMENTS_NAMES:
        INSTRUMENTS.append((instrument_name[:3],instrument_name[-3:]))
    
    ''' ---------- DOWNLOADING DATA ---------- '''
    # Start downloading data with a new process in the background
    analyse_data = multiprocessing.Process(target=Download_and_analyse_data, args=(INSTRUMENTS, RESOLUTION, CORRELATION_PERIODS, API_KEY,CORRELATION_TYPE))
    analyse_data.start()

    ''' ---------- ANTEROS GUI ---------- '''
    # Show plot of prices when clicking a button
    def print_instrument_and_correlation(instrument1, instrument2):
        df_1 = pd.read_json(dir_path + 'df_' + instrument1 + '_temp.json')
        df_2 = pd.read_json(dir_path + 'df_' + instrument2 + '_temp.json')
        P1 = CORRELATION_PERIODS[0]
        P2 = CORRELATION_PERIODS[1]
        type_corr = CORRELATION_TYPE

        # fuction for calculated the spearman correlation
        def rolling_spearman(seqa, seqb, window): 
            """ copy from https://stackoverflow.com/questions/48186624/pandas-rolling-window-spearman-correlation """
            stridea = seqa.to_numpy().strides[0]
            ssa = as_strided(seqa, shape=[len(seqa) - window + 1, window], strides=[stridea, stridea])
            strideb = seqa.to_numpy().strides[0]
            ssb = as_strided(seqb, shape=[len(seqb) - window + 1, window], strides =[strideb, strideb])
            ar = pd.DataFrame(ssa)
            br = pd.DataFrame(ssb)
            ar = ar.rank(1)
            br = br.rank(1)
            corrs = ar.corrwith(br, 1)
            return pad(corrs, (window - 1, 0), 'constant', constant_values=np.nan)

        # Create a small dataframe with the close price of the two instruments
        data_corr = [df_1.close, df_2.close]
        df_corr = pd.concat(data_corr, axis=1, keys=['Close','Close_aux'])
        # Calculate the correlation
        if type_corr == 'pearson':
            df_corr['corr_P1'] = df_corr['Close'].rolling(P1).corr(df_corr['Close_aux']) # pandas in-built function
            df_corr['corr_P2'] = df_corr['Close'].rolling(P2).corr(df_corr['Close_aux']) # pandas in-built function
        elif type_corr == 'spearman': # taking from https://stackoverflow.com/questions/48186624/pandas-rolling-window-spearman-correlation
            df_corr['corr_P1'] = rolling_spearman(df_corr.Close, df_corr.Close_aux, P1)
            df_corr['corr_P2'] = rolling_spearman(df_corr.Close, df_corr.Close_aux, P2)
        
        # Name of graph
        mainTitle = f'\nCORRELATION BETWEEN {instrument1.upper()} AND {instrument2.upper()}'
        subTitle = f'\nLast Bar Closed at {df_1.index[-1].strftime("%H:%M:%S")} shown'

        # Ploting labels as scatter symbols
        def list_scatters(df, P1, P2 ):
            """ list of scatters point for show period"""
            min_price = df[-P2-P1:].low.min()
            max_price = df[-P2-P1:].high.max()
            mid_price = (min_price + max_price) / 2
            signal1 = np.full(P1+P2, np.nan)
            if df.close[-P1] > mid_price:
                signal1[-P1] = (mid_price+min_price)/2
            else:
                signal1[-P1] = (mid_price+max_price)/2
            signal2 = np.full(P1+P2, np.nan)
            if df.close[-P2] > mid_price:
                signal2[-P2] = (mid_price+min_price)/2
            else:
                signal2[-P2] = (mid_price+max_price)/2
            return [signal1, signal2]

        signal_corr1 = np.full(P1+P2, np.nan)
        signal_corr1[-1] = 0 #df_corr.corr_P1[-1]
        signal_corr2 = np.full(P1+P2, np.nan)
        signal_corr2[-1] = 0 #df_corr.corr_P2[-1]
        
        
        # Plotting the range of price
        # 0. Aux instrument candle graph
        # 1. rolling correlation for P1
        # 2. rolling correlation for P2
        # 3. and 4. plot labels as scatter symbols
        aux_df = [ mpf.make_addplot(df_2[-P2-P1:],panel=1, ylabel=instrument2, type='candle'),
                mpf.make_addplot(df_corr['corr_P1'][-P2-P1:], panel=2, ylabel=f'corr\n{P1}',ylim=(-1,1), color='black'),
                mpf.make_addplot(df_corr['corr_P2'][-P2-P1:], panel=3, ylabel=f'corr\n{P2}',ylim=(-1,1), color='black'),
                mpf.make_addplot(list_scatters(df_1,P1,P2)[0], scatter=True, panel=0, markersize=1000, marker=f'$➜{P1}$', color='gray'),
                mpf.make_addplot(list_scatters(df_1,P1,P2)[1], scatter=True, panel=0, markersize=1000, marker=f'$➜{P2}$', color='gray'),
                mpf.make_addplot(list_scatters(df_2,P1,P2)[0], scatter=True, panel=1, markersize=1000, marker=f'$➜{P1}$', color='gray'),
                mpf.make_addplot(list_scatters(df_2,P1,P2)[1], scatter=True, panel=1, markersize=1000, marker=f'$➜{P2}$', color='gray'),
                mpf.make_addplot(signal_corr1, scatter=True, panel=2, markersize=1000, marker=f'${round(df_corr.corr_P1[-1],2)}$', color='gray', ylim=(-1,1)),
                mpf.make_addplot(signal_corr2, scatter=True, panel=3, markersize=1000, marker=f'${round(df_corr.corr_P2[-1],2)}$', color='gray', ylim=(-1,1))
                ]

        kwargs = dict( type='candle',
                    show_nontrading=False,
                    main_panel=0, 
                    panel_ratios=(2,2,1,1), 
                    title= mainTitle+subTitle,
                    ylabel=instrument1, 
                    figratio=(25,20),
                    figscale=1.3,
                    warn_too_much_data= 300000
                    )
                    #xrotation=30,
                    #tight_layout=False,
                    #axisoff=False,
                    #block=False,
                    #warn_too_much_data= 300000
                    #block=False to not block and the script continues
                    #fontscale?
        mpf.plot(df_1[-P2-P1:],**kwargs, addplot=aux_df)
        #mpf.plot(df_loaded,**kwargs, addplot=plot_range, savefig=dir_path+'instrument_overview.png')
        mpf.show()
    
    gui_color = "white" # "white" or "lemon chiffon"
    
    root.configure(background = gui_color)

    '''Main Title'''
    title_label = tk.Label(root, text = f'{CORRELATION_TYPE.upper()} CORRELATION FOR PERIODS {CORRELATION_PERIODS[0]} AND {CORRELATION_PERIODS[1]}')
    title_label.grid(row=0, column=0, columnspan = len(INSTRUMENTS_NAMES) + 4, sticky="NSEW")
    title_label.config(font=('Helvatical bold',18))

    '''Names of instruments upper side'''
    place_column = 2
    place_row = 2
    dict_label_upper ={}
    for item in INSTRUMENTS_NAMES:
        dict_label_upper[(place_row, place_column )] = tk.Label(root, text=item, height=1, width=6, bg=gui_color, fg="maroon")
        dict_label_upper[(place_row, place_column )].grid(row=place_row, column=place_column, sticky="NSEW")
        root.grid_columnconfigure(place_column,weight=1)
        place_column += 1
    
    '''Names of instruments left side'''
    place_column = 1
    place_row = 3
    dict_label_left ={}
    for item in INSTRUMENTS_NAMES:
        dict_label_left[(place_row, place_column )] = tk.Label(root, text=item, height=6, width=2, wraplength=1, bg=gui_color, fg="maroon")
        dict_label_left[(place_row, place_column )].grid(row=place_row, column=place_column,sticky="NSEW")
        root.grid_rowconfigure(place_row,weight=1)
        place_row += 1
    
    '''Names of instruments lower side'''
    place_column = 2
    place_row = len(INSTRUMENTS_NAMES) + 3
    dict_label_lower ={}
    for item in INSTRUMENTS_NAMES:
        dict_label_lower[(place_row, place_column )] = tk.Label(root, text=item, height=1, width=6, bg=gui_color, fg="maroon")
        dict_label_lower[(place_row, place_column )].grid(row=place_row, column=place_column, sticky="NSEW")
        root.grid_columnconfigure(place_column,weight=1)
        place_column += 1
    
    '''Names of instruments right side'''
    place_column = len(INSTRUMENTS_NAMES) + 2
    place_row = 3
    dict_label_right ={}
    for item in INSTRUMENTS_NAMES:
        dict_label_right[(place_row, place_column )] = tk.Label(root, text=item, height=6, width=2, wraplength=1, bg=gui_color, fg="maroon")
        dict_label_right[(place_row, place_column )].grid(row=place_row, column=place_column,sticky="NSEW")
        root.grid_rowconfigure(place_row,weight=1)
        place_row += 1

    '''Buttons definition for correlations'''
    place_column = 2
    dict_buttons = {}
    # Creating a dictionary of buttons for create the matrix of correlation
    for item in INSTRUMENTS_NAMES:
        place_row = 3
        for item_corr in INSTRUMENTS_NAMES:
            correlation_name = item +'_'+item_corr
            if item != item_corr:
                dict_buttons[correlation_name] = tk.Button(root,  text = 'loading...', command=partial(print_instrument_and_correlation,item, item_corr), padx=15, pady=15, borderwidth=25, height = 1 , width = 1)
                dict_buttons[correlation_name].grid(row= place_row, column=place_column, sticky=None) 
                myFont = font.Font(size=20)
                dict_buttons[correlation_name]['font'] = myFont
            else:
                dict_buttons[correlation_name] = tk.Button(root,  text = f'     P1={CORRELATION_PERIODS[0]} ➚\n\n\n⬋ P2={CORRELATION_PERIODS[1]}', state=tk.DISABLED, justify='left')#, padx=15, pady=15,  height = 1 , width = 1)
                dict_buttons[correlation_name].grid(row= place_row, column=place_column, sticky='NSEW') 
                myFont = font.Font(size=15)
                dict_buttons[correlation_name]['font'] = myFont
            place_row += 1
        place_column += 1
    

    '''Updating values of correlation'''
    def update_buttons():
        """ This function updates the values of the correlation buttons and is always activated every x miliseconds """
        if datetime.datetime.now().second < 10 and datetime.datetime.now().minute % time_frame == 0: # close to minute multiple of dataframe show only "downloading"
             for item in INSTRUMENTS_NAMES:
                    for item_corr in INSTRUMENTS_NAMES:
                        correlation_name = item +'_'+item_corr
                        if item != item_corr:
                            # Changing the porperties of GUI bottons
                            dict_buttons[correlation_name].config(text = 'loading...') # given time to download new values
        else:
            try: # if there is no file, the program will wait
                with open(dir_path + 'CorrelationMatrixDouble' + '_' + RESOLUTION +'.json', 'r') as read_txt:
                    correlation_matrix=json.loads(read_txt.read())
                for item in INSTRUMENTS_NAMES:
                    for item_corr in INSTRUMENTS_NAMES:
                        name_data_frame = 'df_' + item + '_temp'
                        temp_df = pd.read_json(dir_path + name_data_frame +'.json')
                        last_minute_downloaded = temp_df.index[-1].minute
                        correlation_name = item +'_'+item_corr
                        if item != item_corr: # not correlations with itself
                            text_myButton = str(correlation_matrix[item][item_corr])
                            r1,g1,b1 = color_gradient_correlation_magenta_blue(float(text_myButton), 200) # color of the border
                            if last_minute_downloaded != Last_bar_close(time_frame):
                                text_myButton += ' updating'
                                myFont = font.Font(size=12)
                                dict_buttons[correlation_name]['font'] = myFont
                            else:
                                myFont = font.Font(size=20)
                                dict_buttons[correlation_name]['font'] = myFont
                            r2,g2,b2 = 0, 0, 0 # text color
                            #r2,g2,b2 = color_gradient_correlation_yellow_green(-1*float(text_myButton), 0) # I tried the text in another colors
                            # Changing the porperties of GUI bottons
                            dict_buttons[correlation_name].config(text = text_myButton, highlightbackground=rgb_to_hex(r1,g1,b1), fg=rgb_to_hex(r2,g2,b2), padx=15, pady=15, borderwidth=25,  height = 1, width = 1 ) #borderwidth=10,
                        else:
                            r1,g1,b1 = color_gradient_correlation_magenta_blue(0, 200)
                            r2,g2,b2 = 0, 0, 0
                            # Diagonal bottons are different
                            dict_buttons[correlation_name].config(highlightbackground=rgb_to_hex(r1,g1,b1), fg=rgb_to_hex(r2,g2,b2)) #borderwidth=10,

            except:
                # if there is no file to read, the program will wait
                root.after(1000, update_buttons)
            
        # wait and run the function again in diferent intervals
        if datetime.datetime.now().second > 11 and datetime.datetime.now().second < 49:
            root.after(10000, update_buttons)
        else:
            root.after(2000, update_buttons)
    
    root.after(15000, update_buttons) # the first time the function is run then inside the fuction the command for run it again and again is in itself
    
    root.mainloop()

    """ ========================= END OF PROGRAM ========================= """

# Color gradient from -1 to 1, from magenta to blue
def color_gradient_correlation_magenta_blue(temp_correlation,color_grey):
    return (int(255*(1-max(0,temp_correlation))-(255-color_grey)*(1-abs(temp_correlation))),
        int(color_grey*(1-abs(temp_correlation))),
        int(255-(255-color_grey)*(1-abs(temp_correlation)))
        )

# Color gradient from -1 to 1, from yellow to green
# This gradient color are the complementary for magenta-blue gradient
# This fuction is not used
def color_gradient_correlation_yellow_green(temp_correlation,color_grey):
    saturation = 200
    return (int(saturation*(1-max(0,temp_correlation))-(saturation-color_grey)*(1-abs(temp_correlation))),
        int(saturation-(saturation-color_grey)*(1-abs(temp_correlation))),
        int(color_grey*(1-abs(temp_correlation))),
        )

# from RGB to hexagecimal
def rgb_to_hex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

# Download data from AlphaVantage periodically
# This is a process in parallel with main fuction
def Download_and_analyse_data(INSTRUMENTS, RESOLUTION, CORRELATION_PERIODS, input_api_key, CORRELATION_TYPE):
    # Time frame values are supported: 5min, 15min, 30min, 60min
    if RESOLUTION == '5min':
            time_frame = 5
    elif RESOLUTION == '15min':
        time_frame = 15
    elif RESOLUTION == '30min':
        time_frame = 30
    elif RESOLUTION == '60min':
        time_frame = 60
    # Local difference with UTC
    local = datetime.datetime.now()
    utc = datetime.datetime.utcnow()
    utc_delta = int((local - utc).days * 86400 + round((local - utc).seconds, -1))
    utc_delta = round(utc_delta/3600)
    # Download data from AlphaVantage returns a panda dataframe manipulated for our propourse
    def Download_Data_AlphaVantage(from_symbol, to_symbol, interval, utc_delta):
        """ For the moment this request only valid for forex symbols"""
        # requesting data from AlphaVantage
        API_KEY = input_api_key # get it from https://www.alphavantage.co/support/#api-key
        function = "FX_INTRADAY" # Forex
        
        if 2*max(CORRELATION_PERIODS) + min(CORRELATION_PERIODS) > 100:
            outputsize = "full" # download all available data
        else:
            outputsize = "compact" # download only last 100 data points
        datatype = "csv"
        url = f"https://www.alphavantage.co/query?function={function}&from_symbol={from_symbol}&to_symbol={to_symbol}&interval={interval}&apikey={API_KEY}&datatype={datatype}&outputsize={outputsize}"
        res = requests.get(url)
        # the CSV file content is all available in the reponse
        df_response = pd.read_csv(io.StringIO(res.content.decode()), parse_dates=['timestamp'], index_col='timestamp').sort_index()
        # Deleting last value of not closed bar
        df_response.drop(df_response.index[-1], inplace=True) 
        # changing the index to local time
        df_response.index = df_response.index + datetime.timedelta(hours=utc_delta)

        return df_response

    # Creating a matrix with correlation values diagonal upper is for CORRELATION_PERIODS[0] and lower diagonal are correlation for period CORRELATION_PERIODS[1]
    def Correlation_Matrix_Doble(CORRELATION_PERIODS, INSTRUMENTS, df_dict, method):
        dict_CorrelationMatrix = {}
        for PeriodCorrelation in CORRELATION_PERIODS:
            temp_prices_dict = {}
            for from_symbol, to_symbol in INSTRUMENTS:
                instrument = from_symbol + to_symbol 
                temp_prices_dict[instrument] = df_dict[instrument]['close'][-PeriodCorrelation:].tolist()
            df_correlation_prices = pd.DataFrame(temp_prices_dict)
            CorrelationMatrix = df_correlation_prices.corr(method = method).round(2)
            dict_CorrelationMatrix[PeriodCorrelation] = CorrelationMatrix
        # Creating a matrix correlation but half is one period and half is the other
        CorrelationMatrixDouble = dict_CorrelationMatrix[CORRELATION_PERIODS[0]].copy()
        for i in range(len(INSTRUMENTS)):
            CorrelationMatrixDouble.iloc[i:, i] = dict_CorrelationMatrix[CORRELATION_PERIODS[1]].iloc[i:, i]
            CorrelationMatrixDouble.iloc[i, i] = 0 # for simplified the use later
        return CorrelationMatrixDouble

    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/' # For saving downloaded data
    df_dict={}
    while True:
        ''' Downloading historical data of instruments'''
        df_dict={}
        for from_symbol, to_symbol in INSTRUMENTS: 
            #print('>>>',from_symbol, to_symbol,'<<<')
            # download the instrument and check if the last bar closed is the same of the downloaded
            waiting = 1
            while True: 
                time.sleep(waiting)
                try:
                    df_response = Download_Data_AlphaVantage(from_symbol,to_symbol,RESOLUTION,utc_delta)
                    last_minute_downloaded = df_response.index[-1].minute
                    if last_minute_downloaded == Last_bar_close(time_frame):
                        #print('download',from_symbol, to_symbol,'at',datetime.datetime.now().isoformat(timespec='seconds', sep=' '), 'with',waiting,'times trying')
                        break
                except: #error downloading data, trying again
                    pass
                    #print('error while downloading data',from_symbol, to_symbol, 'at', datetime.datetime.now().isoformat(timespec='seconds', sep=' '))
                waiting += 1
            # Adding the data frame to a dictionary for access    
            df_dict[from_symbol+to_symbol] = df_response
            # Saving df_response to json
            df_response.to_json(dir_path + 'df_' + from_symbol+to_symbol + '_temp.json')

        '''Correlation Matrix'''
        CorrelationMatrixDouble = Correlation_Matrix_Doble(CORRELATION_PERIODS, INSTRUMENTS, df_dict, CORRELATION_TYPE)
        CorrelationMatrixDouble.to_json(dir_path + 'CorrelationMatrixDouble' + '_' + RESOLUTION + '.json')

        '''Waiting for the moment for starting a new candle'''
        # wait until you are near at the start of a new minute
        while datetime.datetime.now().second > 3:
            time.sleep(2)
        # wait until you are in the start of a new candle
        while  datetime.datetime.now().minute%time_frame != 0: # one minute less than the time 
            if datetime.datetime.now().second < 45:
                time.sleep(10)
            else:
                time.sleep(1)
        time.sleep(2) # time for ensure the provider of data is ready
        #print('--> starting a new period at',datetime.datetime.now().isoformat(timespec='seconds', sep=' '))

# Last bar close
def Last_bar_close(time_frame):
    minutes_now = datetime.datetime.now().minute
    last_bar_close = minutes_now - minutes_now%time_frame
    return last_bar_close

if __name__ == '__main__':
    main()
    #print('all done')
