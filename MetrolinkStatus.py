import datetime
import time
import json
import urllib2

#Format Arrival Time
def formatArrivalTime(scheduledStop):
    timefmt="%I:%M %p"

    scheduledTime = scheduledStop["FormattedTrainMovementTime"]
    scheduledDateTime = datetime.datetime.strptime(scheduledTime,timefmt)
    
    expectedTime = scheduledStop["FormattedCalcTrainMovementTime"]
    expectedDateTime = datetime.datetime.strptime(expectedTime,timefmt)
    
    scheduleDiff = int((expectedDateTime-scheduledDateTime).total_seconds()/60)

    if scheduleDiff != 0:
        return "*%s (%s)*" % (expectedTime,scheduleDiff)
    else:
        return "%s" % (scheduledTime)

#Push Train Status To Slack
def pushTrainStatusToSlack(slackWebhookURL,slackMessage):
    req = urllib2.Request(slackWebhookURL)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, slackMessage)

# Main
def main():
    #config
    metrolinkStationStatusURL = 'https://rtt.metrolinktrains.com/CIS/LiveTrainMap/JSON/StationScheduleList.json'
    slackWebhookURL = 'PLACE_WEBHOOK_URL_HERE'
    stations = ["TUSTIN","IRVINE"]
    debug = False

    #metrolink line short names
    lineShortName = { "VC LINE": "VT",
                        "91/PV Line": "91",
                        "91PV Line": "91",
                        "AV LINE": "AV",
                        "IE LINE": "IE",
                        "IEOC LINE": "IE",
                        "OC LINE": "OC",
                        "SB LINE": "SB",
                        "VT LINE": "VT"}

    #metrolink train stations
    metrolinkStations = {"ANAHEIM-CANYON": "Anaheim Canyon",
                            "ARTIC": "Anaheim",
                            "BALDWINPARK": "Baldwin Park",
                            "BUENAPARK": "Buena Park",
                            "BURBANK-AIRPORT-NORTH": "Burbank Airport - North",
                            "BURBANK-AIRPORT-SOUTH": "Burbank Airport - South",
                            "CALSTATE": "Cal State LA",
                            "CAMARILLO": "Camarillo",
                            "CHATSWORTH": "Chatsworth",
                            "CLAREMONT": "Claremont",
                            "COMMERCE": "Commerce",
                            "COVINA": "Covina",
                            "DOWNTOWN BURBANK": "Burbank - Downtown",
                            "ELMONTE": "El Monte",
                            "FONTANA": "Fontana",
                            "FULLERTON": "Fullerton",
                            "GLENDALE": "Glendale",
                            "INDUSTRY": "Industry",
                            "IRVINE": "Irvine",
                            "LAGUNANIGUEL-MISSIONVIEJO": "Laguna Niguel/Mission Viejo",
                            "LANCASTER": "Lancaster",
                            "LAUS": "L.A. Union Station",
                            "MAIN-CORONA-NORTH": "Corona - North Main",
                            "MONTCLAIR": "Montclair",
                            "MONTEBELLO": "Montebello/Commerce",
                            "MOORPARK": "Moorpark",
                            "MORENO-VALLEY-MARCH-FIELD": "Moreno Valley/March Field",
                            "NEWHALL": "Newhall",
                            "NORTHRIDGE": "Northridge",
                            "NORWALK/SANTA FE SPRINGS": "Norwalk/Santa Fe Springs",
                            "NORWALK-SANTAFESPRINGS": "Norwalk/Santa Fe Springs",
                            "OCEANSIDE": "Oceanside",
                            "ONTARIO-EAST": "Ontario - East",
                            "ORANGE": "Orange",
                            "OXNARD": "Oxnard",
                            "PALMDALE": "Palmdale",
                            "PEDLEY": "Jurupa Valley/Pedley",
                            "PERRIS-DOWNTOWN": "Perris - Downtown",
                            "PERRIS-SOUTH": "Perris - South",
                            "POMONA-DOWNTOWN": "Pomona - Downtown",
                            "POMONA-NORTH": "Pomona - North",
                            "RANCHO CUCAMONGA": "Rancho Cucamonga",
                            "RIALTO": "Rialto",
                            "RIVERSIDE-DOWNTOWN": "Riverside - Downtown",
                            "RIVERSIDE-HUNTERPARK": "Riverside - Hunter Park/UCR",
                            "RIVERSIDE-LA SIERRA": "Riverside - La Sierra",
                            "SAN BERNARDINO": "San Bernardino",
                            "SANBERNARDINOTRAN": "San Bernardino-Downtown",
                            "SAN CLEMENTE": "San Clemente",
                            "SAN CLEMENTE PIER": "San Clemente Pier",
                            "SAN JUAN CAPISTRANO": "San Juan Capistrano",
                            "SANTA ANA": "Santa Ana",
                            "SANTA CLARITA": "Santa Clarita",
                            "SIMIVALLEY": "Simi Valley",
                            "SUN VALLEY": "Sun Valley",
                            "SYLMAR/SAN FERNANDO": "Sylmar/San Fernando",
                            "TUSTIN": "Tustin",
                            "UPLAND": "Upland",
                            "VAN NUYS": "Van Nuys",
                            "VENTURA-EAST": "Ventura - East",
                            "VIA PRINCESSA": "Via Princessa",
                            "VINCENT GRADE/ACTON": "Vincent Grade/Acton",
                            "WEST CORONA": "Corona - West",
                            "SAN BERNARDINO-DOWNTOWN": "San Bernardino - Downtown"
    }

    #metrolink train statuses
    trainStatus = { "ON TIME":"good",
                    "DELAYED":"warning",
                    "EXTENDED DELAYED":"danger",
                    "CANCELLED":"danger"}

    #fetch metrolink train status
    stationScheduleList = json.load(urllib2.urlopen(metrolinkStationStatusURL))

    #process train statuses
    for station in stations:
        trains = []

        for scheduledStop in stationScheduleList:
            if scheduledStop["PlatformName"] == station :
                if debug:
                    print(
                        '''{
                            "text":"%s %s %s %s on %s",
                            "color":"%s",
                            "mrkdwn_in": ["text"]
                        }''' % ('{:<17}'.format(formatArrivalTime(scheduledStop)), 
                                '{:<2}'.format(lineShortName[scheduledStop["RouteCode"]]), 
                                '{:<6}'.format(scheduledStop["TrainDesignation"]), 
                                scheduledStop["TrainDestination"], 
                                scheduledStop["FormattedTrackDesignation"],
                                trainStatus[scheduledStop["CalculatedStatus"]]))        
                
                trains.append(str(
                    '''{
                        "text":"%s %s %s %s on %s",
                        "color":"%s",
                        "mrkdwn_in": ["text"]
                    }''' % ('{:<17}'.format(formatArrivalTime(scheduledStop)), 
                            '{:<2}'.format(lineShortName[scheduledStop["RouteCode"]]), 
                            '{:<6}'.format(scheduledStop["TrainDesignation"]), 
                            scheduledStop["TrainDestination"], 
                            scheduledStop["FormattedTrackDesignation"], 
                            trainStatus[scheduledStop["CalculatedStatus"]])
                ))

        if len(trains) == 0:
            trains.append("{\"text\":\"No More Scheduled Stops Today\"}")
        
        message = '''{
                        "text": "%s Station - Scheduled Trains",
                        "attachments": [%s]}''' % (metrolinkStations[station]
                            ,",".join(trains))
        
        if debug:
            print(message)

        #push train status to slack
        pushTrainStatusToSlack(slackWebhookURL, message)

main()


