export const offlineCourses = [
    {
        "id": 1,
        "slug": "trading-fundamentals-market-mechanics",
        "title": "Trading Fundamentals & Market Mechanics",
        "category": "TECHNICAL",
        "level": "Beginner",
        "duration_minutes": 90,
        "is_pro": false,
        "short_description": "The bedrock of your trading career. Understand how markets actually work.",
        "learning_objectives": ["Understand Bid/Ask and Spread", "Master Order Types", "Read Candlestick Charts"],
        "modules": [
            {
                "module_id": "1-1",
                "module_title": "Market Basics",
                "lessons": [
                    {
                        "lesson_id": "1-1-1",
                        "lesson_title": "What is a Financial Market?",
                        "content_markdown": "# The Financial Market\n\nUnlike a grocery store where prices are fixed, financial markets are dynamic auctions.\n\n### Key Participants\n- **Banks**: Provide liquidity.\n- **Institutions**: Move the market.\n- **Retail**: You and me (liquidity for the big players).\n\n**Exercise**: Open your charting platform and identify who might be buying at the current support level."
                    },
                    {
                        "lesson_id": "1-1-2",
                        "lesson_title": "Bid, Ask & Spread",
                        "content_markdown": "# The Cost of Business\n\n- **Bid**: The highest price a buyer will pay.\n- **Ask**: The lowest price a seller will accept.\n- **Spread**: The difference (Ask - Bid). This is the broker's fee.\n\n### Formula\n`Spread = Ask Price - Bid Price`"
                    }
                ],
                "module_quiz": [
                    {
                        "question": "What is the Spread?",
                        "options": ["The broker's commission", "The difference between Bid and Ask", "The total volume", "The market open price"],
                        "correct_index": 1,
                        "explanation": "Spread is the gap between the highest buy order and lowest sell order."
                    },
                    {
                        "question": "Who provides the most liquidity?",
                        "options": ["Retail Traders", "Central Banks & Institutions", "Gamblers", "News Agencies"],
                        "correct_index": 1,
                        "explanation": "Institutions transact billions, providing the depth markets need."
                    },
                    {
                        "question": "If Bid is 1.05 and Ask is 1.07, what is the spread?",
                        "options": ["0.01", "0.02", "1.06", "0.005"],
                        "correct_index": 1,
                        "explanation": "1.07 - 1.05 = 0.02."
                    },
                    {
                        "question": "Which price do you buy at?",
                        "options": ["Bid", "Ask", "Mid-market", "Last close"],
                        "correct_index": 1,
                        "explanation": "You buy at the Ask price (what sellers are asking for)."
                    },
                    {
                        "question": "Which price do you sell at?",
                        "options": ["Bid", "Ask", "Mid-market", "Last close"],
                        "correct_index": 0,
                        "explanation": "You sell at the Bid price (what buyers are bidding)."
                    }
                ]
            },
            {
                "module_id": "1-2",
                "module_title": "Order Types",
                "lessons": [
                    {
                        "lesson_id": "1-2-1",
                        "lesson_title": "Market vs Limit Orders",
                        "content_markdown": "# Execution Types\n\n1. **Market Order**: \"Get me in NOW.\" Guarantees fill, not price.\n2. **Limit Order**: \"Get me in specifically AT 1.200\". Guarantees price, not fill.\n\n**Use Limit/Stop orders to avoid slippage.**"
                    },
                    {
                        "lesson_id": "1-2-2",
                        "lesson_title": "Stop Loss & Take Profit",
                        "content_markdown": "# Protection First\n\n- **Stop Loss (SL)**: Your seatbelt. Exits trade if it goes against you.\n- **Take Profit (TP)**: Your paycheck. Exits trade when target is hit.\n\n**Rule**: NEVER enter a trade without an SL."
                    }
                ],
                "module_quiz": [
                    {
                        "question": "A Market Order guarantees...",
                        "options": ["Price", "Fill", "Profit", "Low spread"],
                        "correct_index": 1,
                        "explanation": "Market orders prioritize execution speed over price."
                    },
                    {
                        "question": "A Limit Order guarantees...",
                        "options": ["Price", "Fill", "Execution speed", "No fees"],
                        "correct_index": 0,
                        "explanation": "Limit orders only fill at your specified price or better."
                    },
                    {
                        "question": "What is a Stop Loss?",
                        "options": ["A guaranteed profit", "An automatic exit to limit loss", "A fee paid to brokers", "A type of chart"],
                        "correct_index": 1,
                        "explanation": "It stops your loss from growing."
                    },
                    {
                        "question": "When buying, where is your Stop Loss?",
                        "options": ["Above entry", "Below entry", "At entry", "Nowhere"],
                        "correct_index": 1,
                        "explanation": "If buying, you lose if price drops, so SL is below."
                    },
                    {
                        "question": "When shorting, where is your Take Profit?",
                        "options": ["Above entry", "Below entry", "At entry", "Infinity"],
                        "correct_index": 1,
                        "explanation": "Shorts profit when price falls, so TP is below."
                    }
                ]
            },
            {
                "module_id": "1-3",
                "module_title": "Reading Charts",
                "lessons": [
                    { "lesson_id": "1-3-1", "lesson_title": "Candlestick Anatomy", "content_markdown": "# OHLC\n- **Open**: Start price.\n- **High**: Max price.\n- **Low**: Min price.\n- **Close**: End price.\n\n**Wicks** show rejection. **Body** shows conviction." },
                    { "lesson_id": "1-3-2", "lesson_title": "Timeframes", "content_markdown": "# Fractals\nMarkets are fractal. A Daily candle contains 24 1-hour candles.\n- **Higher Timeframe (HTF)**: Direction.\n- **Lower Timeframe (LTF)**: Entry." }
                ],
                "module_quiz": [{ "question": "Which part of candle shows the range?", "options": ["Body", "Wick", "Color", "Volume"], "correct_index": 1, "explanation": "Wick shows the high and low extremes." }, { "question": "Green candle means...", "options": ["Close < Open", "Close > Open", "High = Low", "No volume"], "correct_index": 1, "explanation": "Price went up." }, { "question": "What constitutes a timeframe?", "options": ["A fixed period per candle", "The total market time", "A specific session", "None"], "correct_index": 0, "explanation": "H1 means each candle is 1 hour." }, { "question": "HTF is used for...", "options": ["Entries", "Scalping", "Overall Direction", "News"], "correct_index": 2, "explanation": "Higher Timeframes show the big picture." }, { "question": "LTF is used for...", "options": ["Entries", "Trend analysis", "Macro", "Fundamentals"], "correct_index": 0, "explanation": "Lower Timeframes help refine entries." }]
            },
            {
                "module_id": "1-4",
                "module_title": "Volume & Volatility",
                "lessons": [
                    { "lesson_id": "1-4-1", "lesson_title": "Understanding Volume", "content_markdown": "# Fuel of the Move\nPrice moves, but volume shows **effort**.\n- High volume + small move = Absorption (Reversal?)\n- High volume + big move = Strength." },
                    { "lesson_id": "1-4-2", "lesson_title": "Sessions & Volatility", "content_markdown": "# When to Trade\n- **London**: High volatility.\n- **NY**: High volatility and reversal.\n- **Asia**: Consolidation.\n\n**Tip**: Don't trade lunch hour if you are scalping." }
                ],
                "module_quiz": [{ "question": "High volume usually confirms...", "options": ["A trend", "A fakeout", "A holiday", "Low liquidity"], "correct_index": 0, "explanation": "Volume validates price movement." }, { "question": "Which trade session has the most volume?", "options": ["London/NY Overlap", "Asia", "Sunday Open", "Late Friday"], "correct_index": 0, "explanation": "Overlap is when both major centers are open." }, { "question": "Low volume usually leads to...", "options": ["Choppy markets", "Explosive moves", "Crashes", "News"], "correct_index": 0, "explanation": "Lack of interest leads to sideways chop." }, { "question": "Volatility is...", "options": ["The direction", "The speed/magnitude of price change", "The cost", "The spread"], "correct_index": 1, "explanation": "Volatility measures how fast price moves." }, { "question": "Best time for volatility?", "options": ["Session Opens", "Lunch", "Holidays", "Weekends"], "correct_index": 0, "explanation": "Opens see the most volume influx." }]
            }
        ],
        "final_exam": {
            "passing_score": 70,
            "questions": [
                { "question": "What is a 'Bid' price?", "options": ["Price you sell at", "Price you buy at", "Mid price", "Future price"], "correct_index": 0, "explanation": "The market Bids to buy from you, so you Sell to the bid." },
                { "question": "What is a Limit Order?", "options": ["Executes immediately at any price", "Executes only at specific price", "Exits a trade", "Adds leverage"], "correct_index": 1, "explanation": "Limit orders wait for price." },
                { "question": "The 'Spread' is paid to...", "options": ["The Bank", "The Broker/Exchange", "The Government", "Yourself"], "correct_index": 1, "explanation": "It's the service fee for matching orders." },
                { "question": "A red candlestick typically means...", "options": ["Price closed lower than open", "Price closed higher", "Market is closed", "High volatility"], "correct_index": 0, "explanation": "Bearish candle." },
                { "question": "Why use a Stop Loss?", "options": ["To lock in profit", "To prevent catastrophic loss", "To enter trades", "To double position"], "correct_index": 1, "explanation": "Risk management tool." },
                { "question": "Which session is known for consolidation?", "options": ["New York", "London", "Asian", "Frankfurt"], "correct_index": 2, "explanation": "Asia is typically slower." },
                { "question": "Timeframe 'M15' means...", "options": ["15 Months", "15 Minutes", "15 Moves", "15 Markets"], "correct_index": 1, "explanation": "15 Minute candle." },
                { "question": "Leverage allows you to...", "options": ["Risk less money", "Control larger position with less capital", "Guarantee wins", "Predict future"], "correct_index": 1, "explanation": "It amplifies buying power." },
                { "question": "What is Liquidity?", "options": ["Water", "How easily you can buy/sell without slippage", "Profit", "Debt"], "correct_index": 1, "explanation": "Ease of transaction." },
                { "question": "Trend is your...", "options": ["Enemy", "Friend", "Broker", "Money"], "correct_index": 1, "explanation": "Trade with the flow." }
            ]
        }
    },
    {
        "id": 2,
        "slug": "intro-price-action",
        "title": "Introduction to Price Action",
        "category": "TECHNICAL",
        "level": "Beginner",
        "duration_minutes": 110,
        "is_pro": false,
        "short_description": "Read the language of the market without indicators.",
        "learning_objectives": ["Identify Trends", "Support & Resistance", "Candle Patterns"],
        "modules": [
            {
                "module_id": "2-1",
                "module_title": "Trend Identification",
                "lessons": [
                    { "lesson_id": "2-1-1", "lesson_title": "HH and HL", "content_markdown": "# Uptrend Anatomy\n- **HH**: Higher High\n- **HL**: Higher Low\n\nAs long as price makes HLs, the trend is up. Do not short." },
                    { "lesson_id": "2-1-2", "lesson_title": "Drawing Trendlines", "content_markdown": "# The Ruler\nConnect at least 2 major swing points. The 3rd touch is often a tradeable bounce.\n**Tip**: Don't force the line. If it cuts through bodies, it's invalid." }
                ],
                "module_quiz": [{ "question": "An uptrend is defined by...", "options": ["LL and LH", "HH and HL", "Flat highs", "Moving averages"], "correct_index": 1, "explanation": "Higher Highs and Higher Lows." }, { "question": "Valid trendlines need...", "options": ["1 point", "2 points", "3 indicators", "Volume"], "correct_index": 1, "explanation": "2 points to draw, 3 to confirm." }, { "question": "In a downtrend, you look to...", "options": ["Buy the dip", "Sell the rally", "Do nothing", "Buy breakout"], "correct_index": 1, "explanation": "Trade with the trend (shorting lower highs)." }, { "question": "Trend ends when...", "options": ["Price touches line", "Structure is broken (LL in uptrend)", "Time expires", "News hits"], "correct_index": 1, "explanation": "Structure break signals reversal." }, { "question": "Steep trendlines are...", "options": ["Sustainable", "Unsustainable/prone to break", "Slow", "Rangebound"], "correct_index": 1, "explanation": "Parabolic moves usually correct." }]
            },
            {
                "module_id": "2-2",
                "module_title": "Support & Resistance",
                "lessons": [
                    { "lesson_id": "2-2-1", "lesson_title": "Horizontal Levels", "content_markdown": "# Memory of Price\nPrice remembers levels. Previous resistance becomes support (Flip).\n\n**Strategy**: Wait for retest of broken resistance." },
                    { "lesson_id": "2-2-2", "lesson_title": "Zones not Lines", "content_markdown": "# Precision is a Myth\nS&R is a zone, not a single pixel line.\nMark the wick high and body close to create a 'zone'." }
                ],
                "module_quiz": [{ "question": "Support is where...", "options": ["Sellers enter", "Buyers enter", "Price accelerates", "Volume dies"], "correct_index": 1, "explanation": "Floor for price." }, { "question": "Resistance becomes Support when...", "options": ["It holds", "It is broken", "It is touched", "Never"], "correct_index": 1, "explanation": "Polarity flip." }, { "question": "S&R should be drawn as...", "options": ["Thin lines", "Zones/Areas", "Circles", "Dots"], "correct_index": 1, "explanation": "Accommodates noise." }, { "question": "Best timeframe for S&R?", "options": ["M1", "M5", "H4/Daily", "S1"], "correct_index": 2, "explanation": "Higher timeframes are stronger." }, { "question": "Fakeout is...", "options": ["Clean break", "Price pokes through then reverses", "Trend continuation", "Gap"], "correct_index": 1, "explanation": "Liquidity grab." }]
            },
            {
                "module_id": "2-3",
                "module_title": "Candlestick Patterns",
                "lessons": [
                    { "lesson_id": "2-3-1", "lesson_title": "Pinbars & Dojis", "content_markdown": "# Rejection Signals\n- **Pinbar**: Long wick = Rejection.\n- **Doji**: Indecision.\n\nCombined with S&R, these are powerful triggers." },
                    { "lesson_id": "2-3-2", "lesson_title": "Engulfing Bars", "content_markdown": "# Momentum Shift\nWhen a green candle completely 'eats' the previous red one. Shows buyers have totally overwhelmed sellers." }
                ],
                "module_quiz": [{ "question": "Long wick to the upside indicates...", "options": ["Buying pressure", "Selling pressure/Rejection", "Indecision", "Trend"], "correct_index": 1, "explanation": "Sellers pushed price back down." }, { "question": "Doji means...", "options": ["Strong trend", "Market is closed", "Indecision/Balance", "Reversal only"], "correct_index": 2, "explanation": "Open equals Close (roughly)." }, { "question": "Bullish Engulfing is strong at...", "options": ["Resistance", "Support", "Middle of nowhere", "Downtrend start"], "correct_index": 1, "explanation": "Reversal signal at support." }, { "question": "Pattern reliability increases with...", "options": ["Lower timeframe", "Higher timeframe", "More indicators", "Less volume"], "correct_index": 1, "explanation": "Daily signals > 1-minute signals." }, { "question": "Don't trade patterns...", "options": ["In isolation", "With context", "At key levels", "With trend"], "correct_index": 0, "explanation": "Always need context (Level + Pattern)." }]
            },
            {
                "module_id": "2-4",
                "module_title": "Chart Patterns",
                "lessons": [
                    { "lesson_id": "2-4-1", "lesson_title": "Double Top/Bottom", "content_markdown": "# The 'M' and 'W'\n- **Double Top (M)**: Reversal at highs.\n- **Double Bottom (W)**: Reversal at lows.\n\nWait for neckline break." },
                    { "lesson_id": "2-4-2", "lesson_title": "Flags & Pennants", "content_markdown": "# Continuation\nAfter a strong move (pole), price consolidates (flag). The break usually continues the original direction." }
                ],
                "module_quiz": [{ "question": "Double Top is a...", "options": ["Continuation pattern", "Reversal pattern", "Range pattern", "News event"], "correct_index": 1, "explanation": "Reverses an uptrend." }, { "question": "Bull Flag targets...", "options": ["Down", "Sideways", "Up (measured move)", "Zero"], "correct_index": 2, "explanation": "Continuation up." }, { "question": "Head and Shoulders is...", "options": ["Bullish", "Bearish Reversal", "Neutral", "Continuation"], "correct_index": 1, "explanation": "Classic reversal." }, { "question": "Trade the pattern when...", "options": ["It starts", "It breaks out/confirms", "It fails", "Randomly"], "correct_index": 1, "explanation": "Wait for confirmation." }, { "question": "Target for flag is...", "options": ["The flag size", "The pole length", "Double the move", "10 pips"], "correct_index": 1, "explanation": "Measured move of the pole." }]
            }
        ],
        "final_exam": {
            "passing_score": 70,
            "questions": [
                { "question": "Higher Highs and Higher Lows define...", "options": ["Downtrend", "Uptrend", "Range", "Correction"], "correct_index": 1, "explanation": "Definition of uptrend." },
                { "question": "A hammer candle at support suggests...", "options": ["Selling", "Buying/Reversal", "Continuation", "Nothing"], "correct_index": 1, "explanation": "Bullish rejection." },
                { "question": "Resistance turned Support is called...", "options": ["Fakeout", "Flip/Polarity Change", "Breakout", "Gap"], "correct_index": 1, "explanation": "S/R Flip." },
                { "question": "Head & Shoulders pattern indicates...", "options": ["Trend ending", "Trend starting", "Trend pausing", "Volatile market"], "correct_index": 0, "explanation": "Reversal." },
                { "question": "Price consolidates in a...", "options": ["Impulse", "Correction/Range", "Crash", "Wick"], "correct_index": 1, "explanation": "Sideways movement." },
                { "question": "Engulfing candle must...", "options": ["Have long wick", "Close above previous open/close range", "Be small", "Be a doji"], "correct_index": 1, "explanation": "It engulfs the previous body." },
                { "question": "Best confirmation for a breakout?", "options": ["Volume spike", "Low volume", "Small candles", "Divergence"], "correct_index": 0, "explanation": "Effort validates move." },
                { "question": "What is a 'Neckline'?", "options": ["A trendline in patterns like High&Shoulders", "Top of chart", "Bottom of chart", "A moving average"], "correct_index": 0, "explanation": "Trigger line for the pattern." },
                { "question": "If trendline breaks, it usually marks...", "options": ["Trend acceleration", "Trend reversal or slowing", "Nothing", "News"], "correct_index": 1, "explanation": "Structure change warning." },
                { "question": "Price Action relies primarily on...", "options": ["Indicators", "Price history and structure", "News feeds", "Algorithms"], "correct_index": 1, "explanation": "Pure price movement." }
            ]
        }
    },
    {
        "id": 3,
        "slug": "smart-money-concepts",
        "title": "Smart Money Concepts (SMC)",
        "category": "TECHNICAL",
        "level": "Advanced",
        "duration_minutes": 240,
        "is_pro": true,
        "short_description": "Trade with the banks. Master Order Blocks, Liquidity, and Imbalance.",
        "learning_objectives": ["Find Order Blocks", "Identify Liquidity Pools", "Trade FVGs"],
        "modules": [
            {
                "module_id": "3-1",
                "module_title": "Liquidity Basics",
                "lessons": [
                    { "lesson_id": "3-1-1", "lesson_title": "What is Liquidity?", "content_markdown": "# The Fuel\nLiquidity = Stop Losses. Banks need your stop loss to fill their massive orders.\n\n- **Buy Side Liquidity (BSL)**: Above highs (stops of shorters).\n- **Sell Side Liquidity (SSL)**: Below lows (stops of buyers)." },
                    { "lesson_id": "3-1-2", "lesson_title": "Inducement", "content_markdown": "# The Trap\nSmart Money creates 'fake' support to induce retail to buy, only to smash through it (taking their stops) to fuel the real move up." }
                ],
                "module_quiz": [{ "question": "Liquidity is essentially...", "options": ["Water", "Pending Orders (Stops/Limits)", "Cash", "Profit"], "correct_index": 1, "explanation": "Orders resting in the market." }, { "question": "Smart Money targets liquidity to...", "options": ["Be mean", "Fill large positions", "Lower spread", "Create trends only"], "correct_index": 1, "explanation": "They need matching orders to enter size." }, { "question": "BSL is found...", "options": ["Above old highs", "Below old lows", "In the middle", "Nowhere"], "correct_index": 0, "explanation": "Stops of those who are short." }, { "question": "SSL is found...", "options": ["Above old highs", "Below old lows", "In the middle", "Nowhere"], "correct_index": 1, "explanation": "Stops of those who are long." }, { "question": "Inducement is...", "options": ["A gift", "A trap to generate liquidity", "A bonus", "A fee"], "correct_index": 1, "explanation": "Luring traders in early." }]
            },
            {
                "module_id": "3-2",
                "module_title": "Market Structure Shift (MSS)",
                "lessons": [
                    { "lesson_id": "3-2-1", "lesson_title": "BOS vs MSS/ChoCH", "content_markdown": "# Structure Breaks\n- **BOS (Break of Structure)**: Trend continuation using body close.\n- **MSS (Market Structure Shift) / ChoCH**: Trend reversal. First sign the tide is turning." },
                    { "lesson_id": "3-2-2", "lesson_title": "Valid Pullbacks", "content_markdown": "# Filtering Noise\nA pullback is only valid if it grabs liquidity from a previous candle. Don't map every single wiggle." }
                ],
                "module_quiz": [{ "question": "BOS implies...", "options": ["Reversal", "Continuation", "Range", "Stop hunt"], "correct_index": 1, "explanation": "Trend continuing." }, { "question": "MSS/ChoCH implies...", "options": ["Reversal potential", "Continuation", "Nothing", "Volume"], "correct_index": 0, "explanation": "Character change." }, { "question": "Valid break requires...", "options": ["Wick only", "Body close", "Touch", "Near miss"], "correct_index": 1, "explanation": "Body close confirms conviction." }, { "question": "Aggressive entry is on...", "options": ["BOS", "ChoCH", "News", "Random"], "correct_index": 1, "explanation": "First sign of reversal." }, { "question": "Don't look for ChoCH in...", "options": ["Zones", "Middle of range", "Key levels", "High volume"], "correct_index": 1, "explanation": "Low probability in noise." }]
            },
            {
                "module_id": "3-3",
                "module_title": "Order Blocks (OB)",
                "lessons": [
                    { "lesson_id": "3-3-1", "lesson_title": "Identifying OBs", "content_markdown": "# The Footprint\nThe last contrary candle before a strong impulsive move that breaks structure.\n- **Bullish OB**: Last sell candle before boom.\n- **Bearish OB**: Last buy candle before crash." },
                    { "lesson_id": "3-3-2", "lesson_title": "Refining OBs", "content_markdown": "# Precision\nOn LTF, a massive Daily OB might be a small specific candle. Refine to reduce risk and increase R:R." }
                ],
                "module_quiz": [{ "question": "Bullish OB is...", "options": ["Last Up candle before Drop", "Last Down candle before Rally", "A Doji", "Hammer"], "correct_index": 1, "explanation": "Institution selling to buy." }, { "question": "OB must cause...", "options": ["A range", "BOS / Imbalance", "A wick", "Confusion"], "correct_index": 1, "explanation": "Must show displacement." }, { "question": "Mitigation means...", "options": ["Price touches OB and reacts", "Price ignores OB", "Price ranges", "Price crashes"], "correct_index": 0, "explanation": "Orders are filled/closed." }, { "question": "Don't optimize OBs...", "options": ["Too much (missing trades)", "Too little", "At all", "Ever"], "correct_index": 0, "explanation": "If too small, you might get missed." }, { "question": "Stop loss goes...", "options": ["At OB open", "Distal line (far edge) of OB", "Randomly", "ENTRY"], "correct_index": 1, "explanation": "Invalidated if price passes through." }]
            },
            {
                "module_id": "3-4",
                "module_title": "Fair Value Gaps (FVG)",
                "lessons": [
                    { "lesson_id": "3-4-1", "lesson_title": "Imbalance Anatomy", "content_markdown": "# The Void\nA 3-candle pattern where the wicks of candle 1 and 3 do not overlap. This gap must be filled." },
                    { "lesson_id": "3-4-2", "lesson_title": "Trading FVGs", "content_markdown": "# The Magnet\nPrice is drawn to FVGs to 'rebalance' price. Use them as entry points or targets." }
                ],
                "module_quiz": [{ "question": "FVG is...", "options": ["Inefficiency/Imbalance", "Efficiency", "Consolidation", "Resistance"], "correct_index": 0, "explanation": "Price moved too fast." }, { "question": "FVG is a pattern of...", "options": ["1 candle", "2 candles", "3 candles", "5 candles"], "correct_index": 2, "explanation": "Gap between 1's low and 3's high." }, { "question": "Price tends to...", "options": ["Avoid FVG", "Fill FVG", "Gap over FVG", "Ignore FVG"], "correct_index": 1, "explanation": "Revert to mean/balance." }, { "question": "Inversion FVG happens when...", "options": ["FVG holds", "FVG fails and acts as support/resistance", "FVG disappears", "Never"], "correct_index": 1, "explanation": "Failed supply becomes demand." }, { "question": "FVG is also called...", "options": ["IPA (Inefficiency Price Action)", "RSI", "MACD", "VWAP"], "correct_index": 0, "explanation": "Another term for same concept." }]
            }
        ],
        "final_exam": {
            "passing_score": 75,
            "questions": [
                { "question": "Smart Money primarily seeks...", "options": ["Indicators", "Liquidity", "News", "Chat rooms"], "correct_index": 1, "explanation": "To fill size." },
                { "question": "What is 'Displacement'?", "options": ["Slow move", "Aggressive, high momentum move leaving imbalance", "Range", "Gap down"], "correct_index": 1, "explanation": "Sign of institutional intent." },
                { "question": "EQ (Equilibrium) is...", "options": ["100% retracement", "50% of the range", "0% of range", "The high"], "correct_index": 1, "explanation": "Premium vs Discount." },
                { "question": "Buy in...", "options": ["Premium", "Discount", "Anywhere", "Resistance"], "correct_index": 1, "explanation": "Buy low (Discount)." },
                { "question": "Sell in...", "options": ["Premium", "Discount", "Anywhere", "Support"], "correct_index": 0, "explanation": "Sell high (Premium)." },
                { "question": "A valid BOS requires...", "options": ["Wick break", "Body close break", "Touch", "Sound effect"], "correct_index": 1, "explanation": "Closing price confirms." },
                { "question": "Order Block validates when...", "options": ["It looks nice", "It led to a BOS and FVG", "It is green", "It is huge"], "correct_index": 1, "explanation": "Cause and Effect." },
                { "question": "Swing High is...", "options": ["Lower than neighbors", "Higher than immediate neighbors", "Random", "The open"], "correct_index": 1, "explanation": "Fractal high." },
                { "question": "Asian Session range is often...", "options": ["Targeted (Liquidity)", "Trend setter", "Avoided", "The move"], "correct_index": 0, "explanation": "Often swept by London." },
                { "question": "If FVG is fully filled...", "options": ["It is useless", "It is balanced", "It is invalid", "It explodes"], "correct_index": 1, "explanation": "Price functionality restored." }
            ]
        }
    },
    {
        "id": 4,
        "slug": "trading-psychology",
        "title": "Trading Psychology Under Pressure",
        "category": "PSYCHOLOGY",
        "level": "Advanced",
        "duration_minutes": 120,
        "is_pro": true,
        "short_description": "Master your mind. The strategy is 20%, psychology is 80%.",
        "learning_objectives": ["Conquer FOMO", "Eliminate Revenge Trading", "Think Probabilistically"],
        "modules": [
            {
                "module_id": "4-1",
                "module_title": "The Trader's Brain",
                "lessons": [
                    { "lesson_id": "4-1-1", "lesson_title": "Fight or Flight", "content_markdown": "# Amygdala Hijack\nWhen you lose money, your brain perceives a physical threat. Blood leaves the logic center (Prefrontal Cortex).\n**Solution**: Breathe. Step away. You cannot think logically in this state." },
                    { "lesson_id": "4-1-2", "lesson_title": "Thinking in Probabilities", "content_markdown": "# The Casino Mindset\nA casino doesn't care if it loses one hand. It plays the edge over 1000 hands.\nStop judging success by ONE trade." }
                ],
                "module_quiz": [{ "question": "Trading stress triggers...", "options": ["Digestion", "Fight or Flight", "Sleep", "Happiness"], "correct_index": 1, "explanation": "Biological threat response." }, { "question": "Probabilistic thinking means...", "options": ["Knowing the future", "Accepting uncertainty/randomness", "Guessing", "Gambling"], "correct_index": 1, "explanation": "Any single outcome is uncertain." }, { "question": "The outcome of one trade is...", "options": ["Critical", "Random", "Predictable", "Everything"], "correct_index": 1, "explanation": "Unique event." }, { "question": "Focus on...", "options": ["Process", "Money", "Winning", "News"], "correct_index": 0, "explanation": "Good process leads to results." }, { "question": "Fear comes from...", "options": ["Market", "Not accepting risk", "Broker", "Screen"], "correct_index": 1, "explanation": "If you accept risk, you don't fear." }]
            },
            {
                "module_id": "4-2",
                "module_title": "Emotional Pitfalls",
                "lessons": [
                    { "lesson_id": "4-2-1", "lesson_title": "FOMO", "content_markdown": "# Fear Of Missing Out\nChasing candles. Usually leads to buying the top.\n**Mantra**: \"There will always be another trade.\"" },
                    { "lesson_id": "4-2-2", "lesson_title": "Revenge Trading", "content_markdown": "# Trying to Get Even\nMarket doesn't owe you anything. Revenge trading increases size when you are least capable.\n**Rule**: 2 losses = Done for day." }
                ],
                "module_quiz": [{ "question": "FOMO leads to...", "options": ["Better entries", "Chasing price/Bad entries", "Patience", "Profit"], "correct_index": 1, "explanation": "Buying extended price." }, { "question": "Revenge trading is...", "options": ["Trying to win back losses immediately", "Strategic", "Planned", "Calm"], "correct_index": 0, "explanation": "Emotional reaction to loss." }, { "question": "Best cure for Revenge Trading?", "options": ["Trade bigger", "Walk away/Close screens", "Cry", "Switch pairs"], "correct_index": 1, "explanation": "Reset mental state." }, { "question": "Tilt is...", "options": ["Useful", "State of emotional confusion/anger", "A strategy", "Pinball"], "correct_index": 1, "explanation": "Loss of rational control." }, { "question": "Market owes you...", "options": ["Money", "Respect", "Nothing", "A living"], "correct_index": 2, "explanation": "It is neutral." }]
            },
            {
                "module_id": "4-3",
                "module_title": "Discipline & Routine",
                "lessons": [
                    { "lesson_id": "4-3-1", "lesson_title": "The Trading Plan", "content_markdown": "# Contract with Yourself\nIf you don't have a plan, you are liquidity. Define setups, risk, and times BEFORE the session." },
                    { "lesson_id": "4-3-2", "lesson_title": "Journaling", "content_markdown": "# Feedback Loop\nYou cannot improve what you don't measure. Record deeper than just PnL—record *emotions*." }
                ],
                "module_quiz": [{ "question": "A Trading Plan must be...", "options": ["Created during trading", "Created before trading", "Optional", "Vague"], "correct_index": 1, "explanation": "Pre-defined rules." }, { "question": "Journaling helps...", "options": ["Identify patterns in behavior", "Waste time", "Fill space", "Keep secrets"], "correct_index": 0, "explanation": "Self-improvement tool." }, { "question": "Discipline is...", "options": ["Doing what you want", "Following rules when it's hard", "Being lucky", "Being smart"], "correct_index": 1, "explanation": "Consistency under pressure." }, { "question": "Routine reduces...", "options": ["Profit", "Decision fatigue/Stress", "Wins", "Time"], "correct_index": 1, "explanation": "Automates decisions." }, { "question": "Review trades...", "options": ["Never", "Once a year", "Daily/Weekly", "When winning"], "correct_index": 2, "explanation": "Continuous feedback." }]
            },
            {
                "module_id": "4-4",
                "module_title": "Peak Performance",
                "lessons": [
                    { "lesson_id": "4-4-1", "lesson_title": "Flow State", "content_markdown": "# Zone\nBalance between challenge and skill. To achieve flow, reduce risk to a level where fear vanishes." },
                    { "lesson_id": "4-4-2", "lesson_title": "Lifestyle", "content_markdown": "# Bio-Hacking\nSleep, Diet, Exercise. A tired brain makes bad decisions. Treat trading like elite sport." }
                ],
                "module_quiz": [{ "question": "Flow state requires...", "options": ["High anxiety", "Boredom", "Balance of skill and challenge", "Luck"], "correct_index": 2, "explanation": "Optimal psychology." }, { "question": "Physical health impacts...", "options": ["Nothing", "Decision making capability", "Market direction", "Spread"], "correct_index": 1, "explanation": "Brain is an organ." }, { "question": "Burnout comes from...", "options": ["Overtrading/No breaks", "Winning", "Sleeping", "Eating"], "correct_index": 0, "explanation": "Mental exhaustion." }, { "question": "Meditation helps...", "options": ["Predict price", "Focus and emotional regulation", "Increase leverage", "Scam"], "correct_index": 1, "explanation": "Mindfulness." }, { "question": "Pro traders focus on...", "options": ["Money", "Performance/Execution", "Lambos", "Fame"], "correct_index": 1, "explanation": "Money is a byproduct." }]
            }
        ],
        "final_exam": {
            "passing_score": 80,
            "questions": [
                { "question": "The 'Edge' resides in...", "options": ["One trade", "A large sample size of trades", "Your broker", "Indicators"], "correct_index": 1, "explanation": "Statistical advantage." },
                { "question": "If you feel heart racing, you should...", "options": ["Add to position", "Reduce position/Exit", "Ignore it", "Scream"], "correct_index": 1, "explanation": "You are over-leveraged/emotional." },
                { "question": "Recency Bias is...", "options": ["Being new", "Letting recent trades affect judgment", "Formatting", "None"], "correct_index": 1, "explanation": "Last trade influence." },
                { "question": "Gambler's Fallacy...", "options": ["Believing a win is 'due' after losses", "Counting cards", "Betting small", "Winning"], "correct_index": 0, "explanation": "Independent events." },
                { "question": "Consistency comes from...", "options": ["Consistent feelings", "Consistent actions/rules", "Consistent market", "Luck"], "correct_index": 1, "explanation": "You are the variable." },
                { "question": "Confirmation Bias...", "options": ["Seeking info that supports your view", "Confirming entries", "Being right", "None"], "correct_index": 0, "explanation": "Ignoring counter-evidence." },
                { "question": "Why use a checklist?", "options": ["To slow down", "To ensure all criteria met/remove impulse", "For fun", "Paperwork"], "correct_index": 1, "explanation": "Objective filter." },
                { "question": "Trading is...", "options": ["Easy", "Simple but not easy", "Impossible", "Free money"], "correct_index": 1, "explanation": "Simple rules, hard discipline." },
                { "question": "Your biggest enemy is...", "options": ["Market Makers", "Yourself (Ego/Emotion)", "The Fed", "Twitter"], "correct_index": 1, "explanation": "Self-sabotage." },
                { "question": "Accepting risk means...", "options": ["Understanding you can lose and being OK with it", "Signing a form", "Gambling", "Being brave"], "correct_index": 0, "explanation": "True acceptance eliminates fear." }
            ]
        }
    },
    {
        "id": 5,
        "slug": "risk-management",
        "title": "Basic Risk Management",
        "category": "RISK",
        "level": "Beginner",
        "duration_minutes": 60,
        "is_pro": false,
        "short_description": "Survival is the #1 goal. Learn how to stay in the game.",
        "learning_objectives": ["Understand Position Sizing", "Risk vs Reward", "Drawdown recovery"],
        "modules": [
            {
                "module_id": "5-1",
                "module_title": "The Golden Rules",
                "lessons": [
                    { "lesson_id": "5-1-1", "lesson_title": "The 1% Rule", "content_markdown": "# Longevity\nNever risk more than 1-2% of your account on a single trade. This allows you to survive a losing streak." },
                    { "lesson_id": "5-1-2", "lesson_title": "Risk of Ruin", "content_markdown": "# Math of Loss\nIf you lose 50% of your account, you need +100% gain to get back to breakeven. Don't dig a hole." }
                ],
                "module_quiz": [{ "question": "Recommended max risk per trade?", "options": ["10%", "1-2%", "50%", "All in"], "correct_index": 1, "explanation": "Industry standard for survival." }, { "question": "To recover 50% loss, you need...", "options": ["50% gain", "100% gain", "25% gain", "0% gain"], "correct_index": 1, "explanation": "Math: 100 -> 50. 50 -> 100 is x2." }, { "question": "Capital preservation is...", "options": ["Priority #1", "Optional", "Boring", "For losers"], "correct_index": 0, "explanation": "No capital = No trading." }, { "question": "Drawdown is...", "options": ["Peak to trough decline", "Profit", "Withdrawal", "Trend"], "correct_index": 0, "explanation": "Decline in equity." }, { "question": "Martingale (doubling down) is...", "options": ["Smart", "Dangerous/Account Killer", "Standard", "Safe"], "correct_index": 1, "explanation": "Leads to ruin." }]
            },
            {
                "module_id": "5-2",
                "module_title": "Position Sizing",
                "lessons": [
                    { "lesson_id": "5-2-1", "lesson_title": "The Formula", "content_markdown": "# Don't Guess\n`Size = (Account * Risk%) / (Stop Loss Distance * Pip Value)`\nUse a calculator. Don't eyeball lot sizes." },
                    { "lesson_id": "5-2-2", "lesson_title": "Leverage Kills", "content_markdown": "# Double Edged Sword\nLeverage doesn't change your risk % IF you size correctly. But it tempts you to oversize. Respect it." }
                ],
                "module_quiz": [{ "question": "Position size depends on...", "options": ["Confidene", "Stop Loss Distance & Risk $", "Mood", "Leverage only"], "correct_index": 1, "explanation": "Wider stop = Smaller size." }, { "question": "If SL is wider, size must be...", "options": ["Larger", "Smaller", "Same", "Zero"], "correct_index": 1, "explanation": "To keep risk amount constant." }, { "question": "High leverage is...", "options": ["More profit always", "Risk of faster liquidation", "Safe", "Necessary"], "correct_index": 1, "explanation": "Margin calls happen faster." }, { "question": "Risk per trade should be...", "options": ["Dollar amount or %", "Random", "Based on feeling", "All balance"], "correct_index": 0, "explanation": "Fixed unit." }, { "question": "Lot size for $100 risk 10 pip stop ($10/pip)?", "options": ["1 Lot", "0.1 Lot", "10 Lots", "100 Lots"], "correct_index": 0, "explanation": "100 / (10*10) = 1." }]
            },
            {
                "module_id": "5-3",
                "module_title": "Risk:Reward (RR)",
                "lessons": [
                    { "lesson_id": "5-3-1", "lesson_title": "The Magic of RR", "content_markdown": "# win Rate is Overrated\nWith 1:2 RR, you only need to win 34% of the time to break even. High RR takes pressure off accuracy." },
                    { "lesson_id": "5-3-2", "lesson_title": "Dynamic RR", "content_markdown": "# Reality Check\nDon't set a 1:10 target if structure blocks it. Target logical levels, if RR < 1:2, skip the trade." }
                ],
                "module_quiz": [{ "question": "Min recommended RR?", "options": ["1:0.5", "1:1", "1:2", "1:100"], "correct_index": 2, "explanation": "Allows low win rate success." }, { "question": "With 1:3 RR, 25% win rate is...", "options": ["Profitable", "Breakeven", "Losing", "Impossible"], "correct_index": 1, "explanation": "1 win (3) - 3 losses (3) = 0." }, { "question": "Targeting unrealistic RR leads to...", "options": ["More wins", "Lower win rate/Reversals before TP", "Wealth", "Happiness"], "correct_index": 1, "explanation": "Greed misses exits." }, { "question": "Stop Loss should be based on...", "options": ["Dollar amount", "Structure (Invalidation point)", "Hope", "10 pips flat"], "correct_index": 1, "explanation": "Market dictates stop, not wallet." }, { "question": "Breakeven stop helps...", "options": ["Protect capital", "Lose money", "Get stopped out", "Guarantee win"], "correct_index": 0, "explanation": "Risk free trade." }]
            },
            {
                "module_id": "5-4",
                "module_title": "Portfolio Risk",
                "lessons": [
                    { "lesson_id": "5-4-1", "lesson_title": "Correlation", "content_markdown": "# Everything is Connected\nLong EURUSD and Long GBPUSD = Double Risk on USD weakness. Be aware of improved exposure." },
                    { "lesson_id": "5-4-2", "lesson_title": "Daily Limits", "content_markdown": "# Circuit Breakers\nSet a Max Daily Loss. If hit, software locks you out. Prevents emotional spiral." }
                ],
                "module_quiz": [{ "question": "Correlation means...", "options": ["Assets move together/inverse", "Assets are random", "Assets are same", "None"], "correct_index": 0, "explanation": "Risk exposure links." }, { "question": "Max Daily Loss prevents...", "options": ["Winning", "Blowup days/Tilt", "Trading", "Fees"], "correct_index": 1, "explanation": "Hard stop on bad days." }, { "question": "Diversifying means...", "options": ["Trading same pair", "Trading uncorrelated assets", "Adding size", "Hoppinng"], "correct_index": 1, "explanation": "Spreading risk." }, { "question": "Risk of Ruin calculator uses...", "options": ["Winrate & RR", "Age", "Height", "Broker"], "correct_index": 0, "explanation": "Statistical probability of zero." }, { "question": "Blue Folder news (High Impact) usually...", "options": ["Increases spread/slip", "Is calm", "Is safe", "Is predictable"], "correct_index": 0, "explanation": "Avoid trading news events." }]
            }
        ],
        "final_exam": {
            "passing_score": 85,
            "questions": [
                { "question": "Primary job of a trader?", "options": ["Make money", "Manage Risk", "Predict future", "Beat market"], "correct_index": 1, "explanation": "Risk manager first." },
                { "question": "Why use 1% risk?", "options": ["To get rich slow", "To survive drawdowns", "Broker rule", "Law"], "correct_index": 1, "explanation": "Survival math." },
                { "question": "If you lose 10 trades in a row at 1% risk...", "options": ["You are broke", "You are down ~10%", "You are down 50%", "You are finished"], "correct_index": 1, "explanation": "Manageable drawdown." },
                { "question": "Where do you place SL?", "options": ["Where pain is too much", "Where trade thesis is invalidated", "Arbitrary number", "No SL"], "correct_index": 1, "explanation": "Technical level." },
                { "question": "What is Slippage?", "options": ["Falling", "Difference between expected and filled price", "Fee", "Typo"], "correct_index": 1, "explanation": "Execution variance." },
                { "question": "Holding trades over weekend has...", "options": ["No risk", "Gap risk", "Less risk", "More profit"], "correct_index": 1, "explanation": "Price can gap huge." },
                { "question": "You should withdraw profits...", "options": ["Never", "Regularly (pay yourself)", "When 1M", "When losing"], "correct_index": 1, "explanation": "Realize gains." },
                { "question": "Paper trading is useful for...", "options": ["Generating income", "Testing strategy/Mechanics", "Ego", "Time waste"], "correct_index": 1, "explanation": "Proof of concept." },
                { "question": "The 'Ask' price is...", "options": ["Buy price", "Sell price", "Mid", "Last"], "correct_index": 0, "explanation": "Cost to buy." },
                { "question": "Over-leveraged means...", "options": ["Too much size for account balance", "Too little size", "Strong muscles", "Good strategy"], "correct_index": 0, "explanation": "Risk of ruin high." }
            ]
        }
    },
    {
        "id": 6,
        "slug": "market-structure",
        "title": "Market Structure & Trend Logic",
        "category": "TECHNICAL",
        "level": "Intermediate",
        "duration_minutes": 100,
        "is_pro": false,
        "short_description": "Map the market like a pro using Swing Highs, Lows, and multi-timeframe logic.",
        "learning_objectives": ["Map Structure", "Identify Breaks", "Multi-Timeframe Analysis"],
        "modules": [
            {
                "module_id": "6-1",
                "module_title": "Mapping Structure",
                "lessons": [
                    { "lesson_id": "6-1-1", "lesson_title": "Swing Points", "content_markdown": "# Defining Swings\nA swing high has a lower high on immediate left and right.\nDon't connect every candle. Look for the V and A shapes." },
                    { "lesson_id": "6-1-2", "lesson_title": "Strong vs Weak Highs", "content_markdown": "# Target Selection\n- **Weak High**: Failed to break a low. Likely to be targeted/broken.\n- **Strong High**: Broke a low. Likely to hold." }
                ],
                "module_quiz": [{ "question": "A Strong Low...", "options": ["Breaks structure (High)", "Fails to break", "Is random", "Is weak"], "correct_index": 0, "explanation": "Caused a HH." }, { "question": "Weak Lows are...", "options": ["Support", "Targets (Liquidity)", "Resistance", "Safe stops"], "correct_index": 1, "explanation": "Likely to be run." }, { "question": "Trend continuation expects...", "options": ["Strong points to hold, Weak points to break", "Everything to break", "Range", "Randomness"], "correct_index": 0, "explanation": "Orderflow logic." }, { "question": "Internal Structure is...", "options": ["Noise/Sub-swings", "Major swings", "Daily", "Weekly"], "correct_index": 0, "explanation": "Inside the trading range." }, { "question": "Swing High needs...", "options": ["2 lower highs around it", "2 higher highs around it", "Doji", "Inductor"], "correct_index": 0, "explanation": "Peak formation." }]
            },
            {
                "module_id": "6-2",
                "module_title": "Ranges",
                "lessons": [
                    { "lesson_id": "6-2-1", "lesson_title": "Dealing Range", "content_markdown": "# Fibonacci\nDraw Fib from Swing Low to Swing High.\n- **Premium (>0.5)**: Look to sell.\n- **Discount (<0.5)**: Look to buy." },
                    { "lesson_id": "6-2-2", "lesson_title": "Consolidation", "content_markdown": "# Accumulation\nMarket moves: Impulse -> Correction -> Impulse.\nRange is building energy for the next move." }
                ],
                "module_quiz": [{ "question": "Discount pricing is...", "options": ["Expensive", "Cheap/Below 50%", "Fair", "Premium"], "correct_index": 1, "explanation": "Good for buys." }, { "question": "Premium pricing is...", "options": ["Cheap", "Expensive/Above 50%", "Fair", "Discount"], "correct_index": 1, "explanation": "Good for sells." }, { "question": "Equilibrium is...", "options": ["0%", "100%", "50%", "61.8%"], "correct_index": 2, "explanation": "Midpoint." }, { "question": "In a range, buy...", "options": ["High", "Low", "Middle", "Anywhere"], "correct_index": 1, "explanation": "Buy logic." }, { "question": "Expansion is...", "options": ["Range", "Impulsive move away", "Reversal", "Sleep"], "correct_index": 1, "explanation": "Trend leg." }]
            },
            {
                "module_id": "6-3",
                "module_title": "Multi-Timeframe",
                "lessons": [
                    { "lesson_id": "6-3-1", "lesson_title": "Alignment", "content_markdown": "# Russian Dolls\nTrade when HTF (H4) and LTF (M15) align.\n- H4 Uptrend + M15 BOS Up = High Probability." },
                    { "lesson_id": "6-3-2", "lesson_title": "Counter Trend", "content_markdown": "# Dangers\nTrading LTF bearish in HTF bullish trend is 'Counter Trend'. It is risky and targets should be conservative (recent low)." }
                ],
                "module_quiz": [{ "question": "HTF dictates...", "options": ["Entry", "Overall Bias/Direction", "Spread", "Noise"], "correct_index": 1, "explanation": "Big picture." }, { "question": "LTF provides...", "options": ["Direction", "Precision Entry", "Noise only", "Headache"], "correct_index": 1, "explanation": "Sniper entry." }, { "question": "If H4 is Down and M15 is Up...", "options": ["Buy aggressive", "Wait for M15 to align Down (Pro trend pullback)", "Sell immediately", "Quit"], "correct_index": 1, "explanation": "Wait for alignment." }, { "question": "Alignment increases...", "options": ["Risk", "Probability", "Fees", "Nothing"], "correct_index": 1, "explanation": "Flowing with river." }, { "question": "Top-Down Analysis starts...", "options": ["M1", "Daily/Weekly", "M15", "Tick"], "correct_index": 1, "explanation": "Big to small." }]
            },
            {
                "module_id": "6-4",
                "module_title": "Complex Corrections",
                "lessons": [
                    { "lesson_id": "6-4-1", "lesson_title": "ABC Patterns", "content_markdown": "# Zig Zags\nCorrections are rarely straight lines. Expect A-B-C or W-X-Y shapes before trend resumes." },
                    { "lesson_id": "6-4-2", "lesson_title": "Timing", "content_markdown": "# Patience\nCorrection takes TIME. Impulse is fast. Don't rush into a trade while structure is still developing." }
                ],
                "module_quiz": [{ "question": "Impulses are...", "options": ["Slow", "Fast/Aggressive", "Choppy", "Rare"], "correct_index": 1, "explanation": "Trend moves." }, { "question": "Corrections are...", "options": ["Fast", "Slow/Choppy", "Linear", "Clean"], "correct_index": 1, "explanation": "Resetting orders." }, { "question": "ZigZag is a...", "options": ["Trend", "Correction pattern", "Indicator", "Food"], "correct_index": 1, "explanation": "Corrective shape." }, { "question": "Trade the...", "options": ["Impulse", "Correction", "News", "Noise"], "correct_index": 0, "explanation": "Catch the wave." }, { "question": "Structure protects stops by...", "options": ["Barriers of price", "Hope", "Magic", "Broker"], "correct_index": 0, "explanation": "Swings act as barriers." }]
            }
        ],
        "final_exam": {
            "passing_score": 75,
            "questions": [
                { "question": "Market Structure is...", "options": ["Random", "Orderly sequence of Highs/Lows", "News based", "Indicator"], "correct_index": 1, "explanation": "Framework of price." },
                { "question": "Break of Structure (BOS) signals...", "options": ["Reversal", "Trend Continuation", "Range", "Stop"], "correct_index": 1, "explanation": "Forward progress." },
                { "question": "Why use Top-Down analysis?", "options": ["To confirm entry with higher trend context", "To see more candles", "To waste time", "To confuse"], "correct_index": 0, "explanation": "Context is King." },
                { "question": "If Daily is Bullish, H4 is Bullish, M15 is Bearish...", "options": ["Sell", "Buy dip when M15 turns Bullish", "Do nothing", "Panic"], "correct_index": 1, "explanation": "Pullback buying opportunity." },
                { "question": "A 'Complex Pullback' involves...", "options": ["Straight line", "Multiple legs/structures", "Gap", "One candle"], "correct_index": 1, "explanation": "Corrective structure." },
                { "question": "Golden Zone Fib is...", "options": ["0-10%", "50-61.8% or 62-79%", "100%", "23%"], "correct_index": 1, "explanation": "OTE area." },
                { "question": "Swing Low in uptrend is invalidated if...", "options": ["Wick touches it", "Body closes below it", "Price gets close", "News happens"], "correct_index": 1, "explanation": "Structure breach." },
                { "question": "Internal structure can change trend...", "options": ["Before swing structure", "After swing structure", "Never", "Randomly"], "correct_index": 0, "explanation": "Early warning." },
                { "question": "Fractal nature means...", "options": ["Patterns repeat on all timeframes", "Patterns represent chaos", "Patterns are random", "Charts are broken"], "correct_index": 0, "explanation": "Self-similarity." },
                { "question": "Trade location > Trade...", "options": ["Entry", "Pattern", "Exit", "Direction"], "correct_index": 1, "explanation": "Location (Premium/Discount) is key context." }
            ]
        }
    }
];
