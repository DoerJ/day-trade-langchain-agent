import random
from datetime import datetime, timedelta

def generate_mock_candles(num_candles: int = 60) -> list[dict]:
    candles = []
    base_time = datetime(2024, 5, 24, 9, 30)
    price = 100.0

    for i in range(num_candles):
        open_price = price + random.uniform(-1, 1)
        high_price = open_price + random.uniform(0, 2)
        low_price = open_price - random.uniform(0, 2)
        close_price = random.uniform(low_price, high_price)
        volume = random.randint(10000, 20000)
        candle = {
            "timestamp": (base_time + timedelta(minutes=i)).isoformat(),
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
            "volume": volume
        }
        candles.append(candle)
        price = close_price  # next open is previous close
    
    return candles

# candles now contains 60 dicts
MOCK_CANDLE = generate_mock_candles(80)

# from datetime import datetime, timedelta

# start_time = datetime(2025, 1, 1, 9, 0, 0)

# MOCK_CANDLE = [
#     # === Early base ~4500-4600 (candles 1-8) ===
#     {"open": 4490, "close": 4460, "high": 4510, "low": 4440},
#     {"open": 4460, "close": 4500, "high": 4520, "low": 4450},
#     {"open": 4500, "close": 4480, "high": 4530, "low": 4460},
#     {"open": 4480, "close": 4530, "high": 4550, "low": 4470},
#     {"open": 4530, "close": 4510, "high": 4560, "low": 4500},
#     {"open": 4510, "close": 4560, "high": 4580, "low": 4500},
#     {"open": 4560, "close": 4540, "high": 4590, "low": 4520},
#     {"open": 4540, "close": 4590, "high": 4610, "low": 4530},

#     # === Rally phase 1 toward ~5600 peak (candles 9-18) ===
#     {"open": 4590, "close": 4680, "high": 4700, "low": 4580},
#     {"open": 4680, "close": 4800, "high": 4830, "low": 4670},
#     {"open": 4800, "close": 4950, "high": 4980, "low": 4790},
#     {"open": 4950, "close": 5100, "high": 5130, "low": 4940},
#     {"open": 5100, "close": 5250, "high": 5280, "low": 5090},
#     {"open": 5250, "close": 5400, "high": 5430, "low": 5240},
#     {"open": 5400, "close": 5480, "high": 5520, "low": 5390},
#     {"open": 5480, "close": 5560, "high": 5600, "low": 5460},  # first peak
#     {"open": 5560, "close": 5490, "high": 5580, "low": 5450},
#     {"open": 5490, "close": 5430, "high": 5510, "low": 5400},

#     # === Sharp drop from peak (candles 19-22) ===
#     {"open": 5430, "close": 5100, "high": 5450, "low": 5080},
#     {"open": 5100, "close": 4780, "high": 5120, "low": 4750},
#     {"open": 4780, "close": 4820, "high": 4900, "low": 4700},  # long wick down
#     {"open": 4820, "close": 4760, "high": 4860, "low": 4730},

#     # === Consolidation after drop (candles 23-28) ===
#     {"open": 4760, "close": 4810, "high": 4850, "low": 4740},
#     {"open": 4810, "close": 4780, "high": 4840, "low": 4760},
#     {"open": 4780, "close": 4830, "high": 4870, "low": 4760},
#     {"open": 4830, "close": 4900, "high": 4930, "low": 4820},
#     {"open": 4900, "close": 4860, "high": 4940, "low": 4840},
#     {"open": 4860, "close": 4920, "high": 4960, "low": 4850},

#     # === Rally to second peak ~5400 (candles 29-38) ===
#     {"open": 4920, "close": 5020, "high": 5050, "low": 4910},
#     {"open": 5020, "close": 5130, "high": 5160, "low": 5010},
#     {"open": 5130, "close": 5240, "high": 5270, "low": 5120},
#     {"open": 5240, "close": 5320, "high": 5360, "low": 5230},
#     {"open": 5320, "close": 5380, "high": 5420, "low": 5300},
#     {"open": 5380, "close": 5300, "high": 5410, "low": 5280},  # second peak
#     {"open": 5300, "close": 5220, "high": 5330, "low": 5200},
#     {"open": 5220, "close": 5180, "high": 5260, "low": 5160},
#     {"open": 5180, "close": 5100, "high": 5210, "low": 5080},
#     {"open": 5100, "close": 5050, "high": 5140, "low": 5020},

#     # === Second major decline (candles 39-46) ===
#     {"open": 5050, "close": 4900, "high": 5070, "low": 4880},
#     {"open": 4900, "close": 4750, "high": 4920, "low": 4730},
#     {"open": 4750, "close": 4850, "high": 4880, "low": 4720},
#     {"open": 4850, "close": 4700, "high": 4870, "low": 4680},
#     {"open": 4700, "close": 4580, "high": 4720, "low": 4550},
#     {"open": 4580, "close": 4630, "high": 4660, "low": 4540},
#     {"open": 4630, "close": 4500, "high": 4650, "low": 4460},
#     {"open": 4500, "close": 4150, "high": 4520, "low": 4100},  # deep wick to ~4100

#     # === Bounce attempt (candles 47-53) ===
#     {"open": 4150, "close": 4350, "high": 4400, "low": 4130},
#     {"open": 4350, "close": 4500, "high": 4540, "low": 4330},
#     {"open": 4500, "close": 4620, "high": 4660, "low": 4490},
#     {"open": 4620, "close": 4720, "high": 4760, "low": 4610},
#     {"open": 4720, "close": 4800, "high": 4840, "low": 4700},
#     {"open": 4800, "close": 4750, "high": 4830, "low": 4720},
#     {"open": 4750, "close": 4680, "high": 4770, "low": 4660},

#     # === Lower highs, choppy decline (candles 54-62) ===
#     {"open": 4680, "close": 4730, "high": 4760, "low": 4660},
#     {"open": 4730, "close": 4660, "high": 4750, "low": 4640},
#     {"open": 4660, "close": 4700, "high": 4730, "low": 4640},
#     {"open": 4700, "close": 4640, "high": 4720, "low": 4620},
#     {"open": 4640, "close": 4680, "high": 4700, "low": 4620},
#     {"open": 4680, "close": 4620, "high": 4700, "low": 4600},
#     {"open": 4620, "close": 4660, "high": 4680, "low": 4600},
#     {"open": 4660, "close": 4600, "high": 4680, "low": 4580},
#     {"open": 4600, "close": 4640, "high": 4660, "low": 4580},

#     # === Final ranging zone ~4530-4600 (candles 63-75) ===
#     {"open": 4640, "close": 4600, "high": 4660, "low": 4580},
#     {"open": 4600, "close": 4570, "high": 4620, "low": 4550},
#     {"open": 4570, "close": 4610, "high": 4630, "low": 4550},
#     {"open": 4610, "close": 4580, "high": 4630, "low": 4560},
#     {"open": 4580, "close": 4560, "high": 4600, "low": 4540},
#     {"open": 4560, "close": 4590, "high": 4610, "low": 4545},
#     {"open": 4590, "close": 4555, "high": 4610, "low": 4535},
#     {"open": 4555, "close": 4575, "high": 4595, "low": 4535},
#     {"open": 4575, "close": 4550, "high": 4590, "low": 4530},
#     {"open": 4550, "close": 4570, "high": 4590, "low": 4530},
#     {"open": 4570, "close": 4545, "high": 4585, "low": 4525},
#     {"open": 4545, "close": 4560, "high": 4580, "low": 4525},
#     {"open": 4560, "close": 4538, "high": 4575, "low": 4520},  # final close ~4538
# ]

# # Attach timestamps (1-min intervals)
# for i, candle in enumerate(MOCK_CANDLE):
#     candle["timestamp"] = start_time + timedelta(minutes=i)
# Output: Total candles: 75