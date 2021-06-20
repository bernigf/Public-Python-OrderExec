import os
import sys
import time

from time import sleep

def SIM_LoadData(FileName) :

	file_name = FileName

	with open(file_name) as f:
		content = f.readlines()
		# you may also want to remove whitespace characters like `\n` at the end of each line
		content = [x.strip() for x in content]

	return content

def SIM_GetTickerData (TICKER_data, TICKER_index) :

    if ( TICKER_index < len(TICKER_data) ) : data_str = TICKER_data[TICKER_index]

    # TRIME price float sub string
    time_str = data_str[:8]

    # TRIME price float sub string
    price_str = data_str[9:20]

    price = float(price_str)

    TICKER_index += 1

    return ( TICKER_index, time_str, price )

def FRAGMENTS_PrintData(PARAM_FragmentData, PARAM_Description) :

    fData =  PARAM_FragmentData

    startFragment = fData[0]
    startPrice = startFragment["price"]

    totalSlippage = 0
    totalSlippageAbove = 0
    totalSlippageBelow = 0
    totalQuantity = 0

    print ""
    print " Printing data from: << " + PARAM_Description + " >>"
    print " ========================================================================================================= "

    for fragment in fData :

        frPrice = fragment["price"]
        frSlippage = frPrice - startPrice
        frQuantity = fragment["quantity"]
    
        totalQuantity += frQuantity 

        totalSlippage += frSlippage
        if(frSlippage > 0) : totalSlippageAbove += frSlippage
        if(frSlippage < 0) : totalSlippageBelow += frSlippage

        str1 = "   Fragment " + str(fragment["fragment_id"]).ljust(4) + " -> Index: " + str(fragment["index"]).ljust(7) + " Time: " + str(fragment["time"]) + "   Price: " + str(fragment["price"]).ljust(9)
        str2 = " Slippage: " + str(frSlippage).ljust(9) + " Quantity: " + str(frQuantity).ljust(7)
        print str1 + str2

    print " ========================================================================================================= "
    print ""
    print " Position start price: " + str(startPrice)
    print " Total quantity: " + str(totalQuantity)
    print ""
    print " Above price slippage: " + str(totalSlippageAbove)
    print " Below price slippage: " + str(totalSlippageBelow)
    print " Total Acumulated Slippage: " + str(totalSlippage)
    print ""

def main() :

    #####################################
    # Default settings

    vQuantity = 1.5
    vTimeMinutes = 20
    vAsset = "BTC"
    vSellSymbol = "USDT"
    vTickerDataFile = "UPTREND.dat"
    vOrderFragmentation = 60
    vFragmentRetentionMax = 3
    vVerboseOutput = True

    vSecondDuration = 0.1

    SIMULATOR_TICKER_data = None
    SIMULATOR_TICKER_len = None
    SIMULATOR_TICKER_index = 0
    
    TIME_SECONDS_counter = 0

    FRAGMENT_SECONDS_counter = 0
    FRAGMENT_SECONDS_max = None
    FRAGMENT_FILLED_counter = 0

    FRAGMENT_data = []

    #####################################

    print ""
    print " >>> Using default " + vAsset + vSellSymbol + " symbol"
    print ""

    #vAssetStr = raw_input(" >>> Asset to BUY [" + vAsset + "] : ")
    #vSellSymbolStr = raw_input(" >>> Sell symbol [" + vSellSymbol + "] : ")
    vQuantityStr = raw_input(" >>> " + vAsset + " Quantity [" + str(vQuantity) + "] : ")
    vTimeMinutesStr = raw_input(" >>> Minutes to enter position [" + str(vTimeMinutes) + "] : ")
    vOrderFragmentationStr = raw_input(" >>> Order fragmentation (in seconds) [" + str(vOrderFragmentation) + "] : ")
    vFragmentRetentionMaxStr = raw_input(" >>> Max fragment retention [" + str(vFragmentRetentionMax) + "] : ")

    print ""
    vTickerDataFileStr = raw_input(" >>> TICKER data file: [" + vTickerDataFile + "] : ")
    vSecondDurationStr = raw_input(" >>> Simulated second duration (in real seconds 0.01 = 100x): [" + str(vSecondDuration) + "] : ")
    print ""

    SIMULATOR_TICKER_data = SIM_LoadData(vTickerDataFile)
    SIMULATOR_TICKER_len = len(SIMULATOR_TICKER_data)
    FIRST_TICKER_data = SIM_GetTickerData(SIMULATOR_TICKER_data, SIMULATOR_TICKER_index)
    FIRST_TICKER_time = FIRST_TICKER_data[1]

    vStartTimeStr = raw_input(" >>> Start at time [" + str(FIRST_TICKER_time) + "] : ")

    print ""

    #if (vAssetStr != "") : vAsset = vAssetStr
    #if (vSellSymbolStr != "") : vSellSymbol = vSellSymbolStr
    if (vQuantityStr != "") : vQuantity = float(vQuantityStr)
    if (vTimeMinutesStr != "") : vTimeMinutes = float(vTimeMinutesStr)
    if (vTickerDataFileStr != "") : vTickerDataFile = vTickerDataFileStr
    if (vSecondDurationStr != "") : vSecondDuration = float(vSecondDurationStr)
    if (vFragmentRetentionMaxStr != "") : vFragmentRetentionMax = float(vFragmentRetentionMaxStr)
    if (vStartTimeStr == "") : vStartTimeStr = str(FIRST_TICKER_time)

    vTimeSeconds = vTimeMinutes * 60
    vOrderFragments = round(vTimeSeconds / vOrderFragmentation)
    vFragmentQuantity = round(vQuantity / vOrderFragments,5)
    FRAGMENT_SECONDS_max = vOrderFragmentation

    h, m, s = map(int, vStartTimeStr.split(":"))
    totalSecs = 3600*h + 60*m + s + vTimeSeconds

    eH = int(totalSecs / 3600)
    eM = int(totalSecs / 60 % 60)
    eS = int(totalSecs % 60)
    if(eH >= 24) : eH -= 24

    vEndTimeStr = str(eH) + ":" + str(eM) + ":" + str(eS)

    print " Position settings -> [ " + vAsset + vSellSymbol + " ] [ Quantity: " + str(vQuantity) + " ] [ TICKER dataFile: " + vTickerDataFile + " ]"
    print "                   -> [ Minutes: " + str(vTimeMinutes) + " ] = [ Seconds: " + str(vTimeSeconds) + " ]"
    print "                   -> [ Order Fragmentation: " + str(vOrderFragmentation) + " secs ] = [ Total Fragments: " + str(vOrderFragments) + " ]"
    print "                   -> [ Total Quantity: " + str(vQuantity) + " ] = [ Fragment quantity: " + str(vFragmentQuantity) + " ]"
    print "                   -> [ Start Time: " + str(vStartTimeStr) + " ] -> [ End Time: " + str(vEndTimeStr) + " ]"
    print "                   -> [ Simulated data lenght: " + str(SIMULATOR_TICKER_len) + " ]"
    print ""

    vVerboseOutputStr = "Y"
    vVerboseOutputStr = raw_input(" >>> Print simulation output (Y/N) [" + vVerboseOutputStr + "] : ")

    if (vVerboseOutputStr == "N") : vVerboseOutput = False

    SIMULATION_done = False
    POSITION_start = False
    
    print ""
    print " ===================================================================================================="
    print " Run 1: Starting simple fragmentation (no strategy) ..."
    print " ===================================================================================================="
    print ""
    
    while (SIMULATION_done == False) :

        TIME_SECONDS_counter += 1

        TICKER_data = SIM_GetTickerData(SIMULATOR_TICKER_data, SIMULATOR_TICKER_index)
        SIMULATOR_TICKER_index = TICKER_data[0]
        TICKER_time = TICKER_data[1]
        TICKER_price = TICKER_data[2]

        FRAGMENT_exec = False

        if(POSITION_start == False) :

            if (TICKER_time == vStartTimeStr) :
                
                POSITION_start = True

                if (vVerboseOutput) :
                    print ""
                    print " START time " + vStartTimeStr + " reached at index: " + str(SIMULATOR_TICKER_index)
                    print ""

        else :

            FRAGMENT_SECONDS_counter += 1

            if (FRAGMENT_SECONDS_counter == FRAGMENT_SECONDS_max) :
                FRAGMENT_exec = True
                FRAGMENT_FILLED_counter += 1
                FRAGMENT_SECONDS_counter = 0
                FRAGMENT_data.append({ "fragment_id" : FRAGMENT_FILLED_counter, "index" : SIMULATOR_TICKER_index, "time" : TICKER_time, "price" : TICKER_price, "quantity" : vFragmentQuantity})
        
        if (vVerboseOutput) :
            
            str1 = "INDEX: " + str(SIMULATOR_TICKER_index).ljust(7) + " FSECS: " + str(FRAGMENT_SECONDS_counter).ljust(4) + " TIME: " + str(TICKER_time) + "   PRICE: " + str(TICKER_price) 
            
            if (FRAGMENT_exec) :
                strF = " -> FILL FRAGMENT(" + str(FRAGMENT_FILLED_counter) + ")" 
            else :
                strF = ""

            print str1 + strF 

        else :

            frFilledP = round(FRAGMENT_FILLED_counter * 100 / vOrderFragments,1)
            simP = round(SIMULATOR_TICKER_index * 100 / SIMULATOR_TICKER_len,1)
            sys.stdout.write("     " + str(SIMULATOR_TICKER_index) + "/" + str(SIMULATOR_TICKER_len) + " -> Data used: " + str(simP) + " % -> Fragments Filled: " + str(FRAGMENT_FILLED_counter) + "/" + str(int(vOrderFragments)) + " = " + str(frFilledP)  + "% \r")
            sys.stdout.flush()

        if (FRAGMENT_FILLED_counter == vOrderFragments) :
            SIMULATION_done = True

        if (SIMULATOR_TICKER_index == SIMULATOR_TICKER_len) :
            SIMULATION_done = True         

        sleep(vSecondDuration)

    FRAGMENTS_SIMPLE_data = FRAGMENT_data

    print ""
    print ""
    print " ===================================================================================================="
    print " Run 2: Starting credit fragmentation strategy ..."
    print " ===================================================================================================="
    print ""

    FRAGMENT_data = []
    FRAGMENT_FILLED_counter = 0
    SIMULATOR_TICKER_index = 0
    POSITION_start = False
    TIME_SECONDS_counter = 0
    SIMULATION_done = False

    FRAGMENT_startPrice = None
    FRAGMENT_credit = 0

    while (SIMULATION_done == False) :

        TIME_SECONDS_counter += 1

        TICKER_data = SIM_GetTickerData(SIMULATOR_TICKER_data, SIMULATOR_TICKER_index)
        SIMULATOR_TICKER_index = TICKER_data[0]
        TICKER_time = TICKER_data[1]
        TICKER_price = TICKER_data[2]

        FRAGMENT_exec = False

        if(POSITION_start == False) :

            if (TICKER_time == vStartTimeStr) :
                
                POSITION_start = True

                if (vVerboseOutput) :
                    print ""
                    print " START time " + vStartTimeStr + " reached at index: " + str(SIMULATOR_TICKER_index)
                    print ""

        else :

            FRAGMENT_SECONDS_counter += 1

            if (FRAGMENT_SECONDS_counter == FRAGMENT_SECONDS_max) :
                
                FRAGMENT_SECONDS_counter = 0

                if (FRAGMENT_FILLED_counter == 0) :
                
                    FRAGMENT_credit += 1
                    FRAGMENT_exec = True
                    FRAGMENT_startPrice = TICKER_price
                    print ""
                    print " FIRST fragment filled at price: " + str(TICKER_price)
                    print ""
                
                else :

                    if(TICKER_price > FRAGMENT_startPrice) :

                        FRAGMENT_credit += 1
                        
                        if (FRAGMENT_credit < vFragmentRetentionMax) :
                            FRAGMENT_exec = False
                        else :
                            FRAGMENT_exec = True

                    else :

                        FRAGMENT_credit += vFragmentRetentionMax
                        FRAGMENT_exec = True

                if (FRAGMENT_exec) :

                    while (FRAGMENT_credit > 0) :

                        FRAGMENT_credit -= 1
                        
                        if (FRAGMENT_FILLED_counter < vOrderFragments) :
                            FRAGMENT_FILLED_counter += 1
                            FRAGMENT_data.append({ "fragment_id" : FRAGMENT_FILLED_counter, "index" : SIMULATOR_TICKER_index, "time" : TICKER_time, "price" : TICKER_price, "quantity" : vFragmentQuantity})
        
        if (vVerboseOutput) :
            
            str1 = "INDEX: " + str(SIMULATOR_TICKER_index).ljust(7) + " FSECS: " + str(FRAGMENT_SECONDS_counter).ljust(4) + " TIME: " + str(TICKER_time) + "   PRICE: " + str(TICKER_price) 
            
            if (FRAGMENT_exec) :
                strF = " -> FILL FRAGMENT(" + str(FRAGMENT_FILLED_counter) + ")" 
            else :
                strF = ""

            print str1 + strF 

        else :

            frFilledP = round(FRAGMENT_FILLED_counter * 100 / vOrderFragments,1)
            simP = round(SIMULATOR_TICKER_index * 100 / SIMULATOR_TICKER_len,1)
            sys.stdout.write("     " + str(SIMULATOR_TICKER_index) + "/" + str(SIMULATOR_TICKER_len) + " -> Data used: " + str(simP) + " % -> Fragments Filled: " + str(FRAGMENT_FILLED_counter) + "/" + str(int(vOrderFragments)) + " = " + str(frFilledP)  + "% \r")
            sys.stdout.flush()

        if (FRAGMENT_FILLED_counter >= vOrderFragments) :
            SIMULATION_done = True

        if (SIMULATOR_TICKER_index == SIMULATOR_TICKER_len) :
            SIMULATION_done = True         

        sleep(vSecondDuration)

    FRAGMENTS_CREDITS_data = FRAGMENT_data

    print ""
    print ""
    print " >>> END of simulation"
    print ""
    print " >>> Position fragments data: "
    FRAGMENTS_PrintData(FRAGMENTS_SIMPLE_data, "Simple fragmentation")
    FRAGMENTS_PrintData(FRAGMENTS_CREDITS_data, "Fragment retention credits")
    print ""

main()
