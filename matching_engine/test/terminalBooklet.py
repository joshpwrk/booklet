import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..')))

import time
import json
from termgraph.module import Data, BarChart, Args, Colors
from matching_engine.util import launch_redis_client
from matching_engine.Instrument import Instrument
from matching_engine.LimitOrder import LimitOrder

def chart_booklet():
    # start client
    instrument = Instrument(launch_redis_client(db=0), 'ETH-$1300-CALL-01012024')

    # create empty orderbook
    rows, cols = 10, 2
    orderBook = [[0 for j in range(cols)] for i in range(rows)]

    # get the updated orderbook
    while True:
        start_time = time.time()
        bucketSize = 10
        for index, value in enumerate(range(bucketSize, 101, bucketSize)):
            # TODO: these two commands are the ones that take a while: could use a pipe 
            bidIds = instrument.get_orders_in_tick(True, value - bucketSize, value)
            askIds = instrument.get_orders_in_tick(False, value - bucketSize, value)

            # break down into prices
            bidJsons = [json.loads(d) for d in instrument.r.mget(bidIds) if d is not None]
            bidsInTick = sum(d["amount"] for d in bidJsons)
            orderBook[index][0] = bidsInTick if (bidsInTick > 0) else 0.001

            askJsons = [json.loads(d) for d in instrument.r.mget(askIds) if d is not None]
            asksInTick = sum(d["amount"] for d in askJsons)
            orderBook[index][1] = asksInTick if (asksInTick > 0) else 0.001


        data = Data(
            orderBook, 
            ["$10", "$20", "$30", "$40", "$50", "$60", "$70", "$80", "$90", "$100"], 
            ["Bids", "Asks"]
        )

        chart = BarChart(
            data,
            Args(
                title="Booklet",
                colors=[Colors.Green, Colors.Red],
                space_between=True,
            ),
        )

        chart.draw()

        print("Execution time:", time.time() - start_time)

        time.sleep(0.05)

chart_booklet()