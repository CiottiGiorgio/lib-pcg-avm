import algokit_utils
import pytest
from algokit_utils import get_localnet_default_account
from algokit_utils.config import config
from algosdk.atomic_transaction_composer import SimulateAtomicTransactionResponse
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.lib_pcg32_exposer_algopy import (
    LibPcg32ExposerAlgopyClient,
    SimulateOptions,
)
from smart_contracts.artifacts.lib_pcg32_exposer_pyteal import (
    LibPcg32ExposerPytealClient,
)
from smart_contracts.artifacts.lib_pcg32_exposer_ts import (
    CreateApplicationArgs as CreateApplicationArgsTs,
)
from smart_contracts.artifacts.lib_pcg32_exposer_ts import (
    Deploy as DeployTs,
)
from smart_contracts.artifacts.lib_pcg32_exposer_ts import (
    DeployCreate as DeployCreateTs,
)
from smart_contracts.artifacts.lib_pcg32_exposer_ts import (
    LibPcg32ExposerTsClient,
)
from smart_contracts.artifacts.lib_pcg32_exposer_ts import (
    UpdateApplicationArgs as UpdateApplicationArgsTs,
)


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    match metafunc.config.getoption("language"):
        case "algopy":
            if "lib_pcg32_client" in metafunc.fixturenames:
                metafunc.parametrize(
                    "lib_pcg32_client", ["lib_pcg32_exposer_algopy_client"]
                )
            if "expected_library_size" in metafunc.fixturenames:
                metafunc.parametrize("expected_library_size", [450])
            if "max_unbounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize(
                    "bit_size,max_unbounded_opup_calls", zip(BIT_SIZES, [76, 38, 20])
                )
            if "max_bounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize(
                    "bit_size,max_bounded_opup_calls", zip(BIT_SIZES, [91, 46, 23])
                )
        case "ts":
            if "lib_pcg32_client" in metafunc.fixturenames:
                metafunc.parametrize(
                    "lib_pcg32_client", ["lib_pcg32_exposer_ts_client"]
                )
            if "expected_library_size" in metafunc.fixturenames:
                metafunc.parametrize("expected_library_size", [1300])
            if "max_unbounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize(
                    "bit_size,max_unbounded_opup_calls", zip(BIT_SIZES, [155, 78, 39])
                )
            if "max_bounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize(
                    "bit_size,max_bounded_opup_calls", zip(BIT_SIZES, [174, 88, 44])
                )
        case "pyteal":
            if "lib_pcg32_client" in metafunc.fixturenames:
                metafunc.parametrize(
                    "lib_pcg32_client", ["lib_pcg32_exposer_pyteal_client"]
                )
            if "expected_library_size" in metafunc.fixturenames:
                metafunc.parametrize("expected_library_size", [570])
            if "max_unbounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize(
                    "bit_size,max_unbounded_opup_calls", zip(BIT_SIZES, [91, 46, 23])
                )
            if "max_bounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize(
                    "bit_size,max_bounded_opup_calls", zip(BIT_SIZES, [106, 53, 27])
                )


@pytest.fixture(scope="session")
def lib_pcg32_exposer_algopy_client(
    algod_client: AlgodClient, indexer_client: IndexerClient
) -> LibPcg32ExposerAlgopyClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = LibPcg32ExposerAlgopyClient(
        algod_client,
        creator=get_localnet_default_account(algod_client),
        indexer_client=indexer_client,
    )

    client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.UpdateApp,
    )
    return client


@pytest.fixture(scope="session")
def lib_pcg32_exposer_ts_client(
    algod_client: AlgodClient, indexer_client: IndexerClient
) -> LibPcg32ExposerTsClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = LibPcg32ExposerTsClient(
        algod_client,
        creator=get_localnet_default_account(algod_client),
        indexer_client=indexer_client,
    )

    client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
        create_args=DeployCreateTs(args=CreateApplicationArgsTs()),
        update_args=DeployTs(args=UpdateApplicationArgsTs()),
    )
    return client


@pytest.fixture(scope="session")
def lib_pcg32_exposer_pyteal_client(
    algod_client: AlgodClient, indexer_client: IndexerClient
) -> LibPcg32ExposerPytealClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = LibPcg32ExposerPytealClient(
        algod_client,
        creator=get_localnet_default_account(algod_client),
        indexer_client=indexer_client,
    )

    client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.UpdateApp,
        allow_update=True,
        allow_delete=True,
    )
    return client


RNG_SEED = b"\x00\x00\x00\x00\x00\x00\x00\x2A"

BIT_SIZES = [8, 16, 32]
# These sequences are generated using the reference C implementation.
UNBOUNDED_SEQUENCE = (
    [
        214,
        169,
        155,
        131,
        173,
        50,
        44,
        215,
        8,
        181,
        217,
        129,
        220,
        150,
        81,
        107,
        218,
        68,
        35,
        196,
        72,
        23,
        208,
        171,
        131,
        33,
        170,
        155,
        20,
        200,
        240,
        11,
        182,
        230,
        245,
        232,
        154,
        111,
        214,
        182,
        162,
        59,
        239,
        156,
        238,
        218,
        58,
        96,
        153,
        213,
        150,
        24,
        34,
        133,
        226,
        148,
        207,
        156,
        239,
        7,
        72,
        153,
        113,
        27,
        128,
        112,
        155,
        48,
        170,
        12,
        31,
        79,
        148,
        118,
        84,
        165,
        251,
        54,
        192,
        64,
        251,
        127,
        62,
        127,
        209,
        134,
        93,
        24,
        50,
        248,
        94,
        150,
        201,
        163,
        177,
        157,
        103,
        186,
        109,
        146,
    ],
    [
        31702,
        50345,
        45723,
        21379,
        24237,
        46642,
        12588,
        51159,
        2056,
        15029,
        7641,
        8321,
        19932,
        56214,
        63569,
        8811,
        60122,
        56900,
        47651,
        47556,
        40008,
        20247,
        9936,
        26539,
        11139,
        41505,
        7082,
        7323,
        1812,
        40136,
        57584,
        17675,
        63670,
        32230,
        17141,
        1256,
        26778,
        55663,
        54998,
        10422,
        4514,
        49979,
        26607,
        29852,
        4846,
        5850,
        44346,
        25440,
        32409,
        18901,
        12438,
        61464,
        40738,
        53893,
        51682,
        35476,
        46031,
        12956,
        21999,
        53767,
        63560,
        47769,
        26737,
        29979,
        49280,
        20336,
        55707,
        49712,
        1450,
        60428,
        21023,
        25679,
        24980,
        24950,
        57428,
        24485,
        13051,
        52790,
        46016,
        9280,
        60923,
        50047,
        32830,
        49535,
        18129,
        8582,
        55901,
        34072,
        41778,
        4856,
        61022,
        41366,
        41673,
        45475,
        56497,
        56221,
        1127,
        7354,
        26989,
        22162,
    ],
    [
        3270867926,
        1795671209,
        1924641435,
        1143034755,
        4121910957,
        1757328946,
        3418829100,
        3589261271,
        2062288904,
        4279450293,
        3045727705,
        1731076225,
        106581468,
        4174699414,
        3841390673,
        251273835,
        3019696858,
        736288324,
        449296931,
        3244538308,
        1174969416,
        3641397015,
        2875008720,
        4043466667,
        2045651843,
        2749407777,
        790240170,
        2421562523,
        2232944404,
        661429448,
        3698712816,
        1346782475,
        2479290550,
        2001698278,
        3801367285,
        3116565736,
        2205968538,
        3024935279,
        106813142,
        879896758,
        3613069730,
        2171454267,
        222390255,
        1872327836,
        132911854,
        2317162202,
        2833100090,
        1905681248,
        3248783001,
        2690927061,
        2157981846,
        3714904088,
        2155912994,
        2393559685,
        463063522,
        1131711124,
        2499589071,
        3247518364,
        3794818543,
        972870151,
        1415116872,
        419609241,
        810313841,
        1259894043,
        3220619392,
        969363312,
        3716012443,
        664453680,
        1680803242,
        2607672332,
        1401049631,
        1589666895,
        2472436116,
        2133811574,
        4272939092,
        3617415077,
        387789563,
        3029126710,
        3899044800,
        16000064,
        2204102139,
        3845243775,
        1756201022,
        2713764223,
        3849864913,
        2560762246,
        2661603933,
        4285629720,
        1826857778,
        3025605368,
        3485724254,
        1068671382,
        403284681,
        2962796963,
        2538593457,
        395500445,
        2921792615,
        509549754,
        3861866861,
        3217053330,
    ],
)
LOWER_BOUNDED_SEQUENCE = (
    [
        168,
        237,
        133,
        196,
        142,
        128,
        148,
        228,
        216,
        163,
        164,
        197,
        247,
        251,
        162,
        151,
        227,
        182,
        249,
        224,
        133,
        235,
        166,
        236,
        156,
        202,
        229,
        192,
        197,
        135,
        175,
        156,
        203,
        245,
        185,
        167,
        166,
        216,
        237,
        140,
        189,
        232,
        187,
        162,
        185,
        216,
        153,
        237,
        172,
        217,
        184,
        141,
        234,
        158,
        218,
        185,
        187,
        251,
        128,
        137,
        157,
        232,
        210,
        190,
        230,
        163,
        128,
        220,
        191,
        153,
        237,
        151,
        184,
        255,
        237,
        171,
        210,
        179,
        190,
        192,
        139,
        163,
        180,
        251,
        134,
        143,
        208,
        232,
        153,
        150,
        159,
        163,
        235,
        168,
        133,
        246,
        147,
        139,
        180,
        244,
    ],
    [
        62958,
        61083,
        52525,
        52033,
        62290,
        58550,
        39328,
        39930,
        37425,
        48274,
        45767,
        53798,
        49447,
        59888,
        44646,
        33910,
        33506,
        34430,
        33939,
        46847,
        36919,
        40195,
        53272,
        34217,
        47016,
        55906,
        48502,
        64497,
        64742,
        52719,
        43015,
        42111,
        53546,
        36680,
        64976,
        37220,
        57763,
        61656,
        51738,
        49106,
        58095,
        49249,
        52588,
        38250,
        33557,
        33441,
        56193,
        32820,
        64339,
        35086,
        44887,
        46401,
        40482,
        46385,
        37550,
        33707,
        35287,
        44924,
        37265,
        56846,
        53143,
        34963,
        34776,
        57067,
        49301,
        56290,
        40610,
        62203,
        48461,
        46386,
        43803,
        42703,
        47833,
        58137,
        58104,
        45165,
        33984,
        58655,
        58102,
        41559,
        59197,
        63775,
        44772,
        65024,
        64484,
        61508,
        40213,
        34360,
        51564,
        43596,
        52953,
        41521,
        62134,
        53364,
        44563,
        44151,
        43035,
        57340,
        40209,
        55060,
    ],
    [
        3270867924,
        4121910955,
        3418829098,
        3589261269,
        4279450291,
        3045727703,
        4174699412,
        3841390671,
        3019696856,
        3244538306,
        3641397013,
        2875008718,
        4043466665,
        2749407775,
        2421562521,
        2232944402,
        3698712814,
        2479290548,
        3801367283,
        3116565734,
        2205968536,
        3024935277,
        3613069728,
        2171454265,
        2317162200,
        2833100088,
        3248782999,
        2690927059,
        2157981844,
        3714904086,
        2155912992,
        2393559683,
        2499589069,
        3247518362,
        3794818541,
        3220619390,
        3716012441,
        2607672330,
        2472436114,
        4272939090,
        3617415075,
        3029126708,
        3899044798,
        2204102137,
        3845243773,
        2713764221,
        3849864911,
        2560762244,
        2661603931,
        4285629718,
        3025605366,
        3485724252,
        2962796961,
        2538593455,
        2921792613,
        3861866859,
        3217053328,
        3799482455,
        2518770771,
        2208089529,
        4196796932,
        2791746944,
        3933732098,
        4159360569,
        4243310988,
        3516423413,
        2221049151,
        2199254042,
        2915240812,
        2754316971,
        3549403517,
        3540021468,
        4079242967,
        2984434596,
        2527880043,
        2574616912,
        3003067395,
        3903230594,
        3165924923,
        3862833299,
        3401219656,
        3966705294,
        3174808174,
        3910581952,
        3139926249,
        2756237672,
        3067494577,
        4150544419,
        2927792990,
        3579130267,
        4228482816,
        2580726910,
        2690059168,
        2834353949,
        2750735577,
        2483465508,
        3946430916,
        2327446262,
        3416156060,
        3691695267,
    ],
)
UPPER_BOUNDED_SEQUENCE = (
    [
        41,
        110,
        6,
        69,
        15,
        1,
        21,
        101,
        89,
        36,
        37,
        70,
        120,
        124,
        35,
        24,
        100,
        55,
        122,
        97,
        6,
        108,
        39,
        109,
        29,
        75,
        102,
        65,
        70,
        8,
        48,
        29,
        76,
        118,
        58,
        40,
        39,
        89,
        110,
        13,
        62,
        105,
        60,
        35,
        58,
        89,
        26,
        110,
        45,
        90,
        57,
        14,
        107,
        31,
        91,
        58,
        60,
        124,
        1,
        10,
        30,
        105,
        83,
        63,
        103,
        36,
        1,
        93,
        64,
        26,
        110,
        24,
        57,
        128,
        110,
        44,
        83,
        52,
        63,
        65,
        12,
        36,
        53,
        124,
        7,
        16,
        81,
        105,
        26,
        23,
        32,
        36,
        108,
        41,
        6,
        119,
        20,
        12,
        53,
        117,
    ],
    [
        30191,
        28316,
        19758,
        19266,
        29523,
        25783,
        6561,
        7163,
        4658,
        15507,
        13000,
        21031,
        16680,
        27121,
        11879,
        1143,
        739,
        1663,
        1172,
        14080,
        4152,
        7428,
        20505,
        1450,
        14249,
        23139,
        15735,
        31730,
        31975,
        19952,
        10248,
        9344,
        20779,
        3913,
        32209,
        4453,
        24996,
        28889,
        18971,
        16339,
        25328,
        16482,
        19821,
        5483,
        790,
        674,
        23426,
        53,
        31572,
        2319,
        12120,
        13634,
        7715,
        13618,
        4783,
        940,
        2520,
        12157,
        4498,
        24079,
        20376,
        2196,
        2009,
        24300,
        16534,
        23523,
        7843,
        29436,
        15694,
        13619,
        11036,
        9936,
        15066,
        25370,
        25337,
        12398,
        1217,
        25888,
        25335,
        8792,
        26430,
        31008,
        12005,
        32257,
        31717,
        28741,
        7446,
        1593,
        18797,
        10829,
        20186,
        8754,
        29367,
        20597,
        11796,
        11384,
        10268,
        24573,
        7442,
        22293,
    ],
    [
        1123384277,
        1974427308,
        1271345451,
        1441777622,
        2131966644,
        898244056,
        2027215765,
        1693907024,
        872213209,
        1097054659,
        1493913366,
        727525071,
        1895983018,
        601924128,
        274078874,
        85460755,
        1551229167,
        331806901,
        1653883636,
        969082087,
        58484889,
        877451630,
        1465586081,
        23970618,
        169678553,
        685616441,
        1101299352,
        543443412,
        10498197,
        1567420439,
        8429345,
        246076036,
        352105422,
        1100034715,
        1647334894,
        1073135743,
        1568528794,
        460188683,
        324952467,
        2125455443,
        1469931428,
        881643061,
        1751561151,
        56618490,
        1697760126,
        566280574,
        1702381264,
        413278597,
        514120284,
        2138146071,
        878121719,
        1338240605,
        815313314,
        391109808,
        774308966,
        1714383212,
        1069569681,
        1651998808,
        371287124,
        60605882,
        2049313285,
        644263297,
        1786248451,
        2011876922,
        2095827341,
        1368939766,
        73565504,
        51770395,
        767757165,
        606833324,
        1401919870,
        1392537821,
        1931759320,
        836950949,
        380396396,
        427133265,
        855583748,
        1755746947,
        1018441276,
        1715349652,
        1253736009,
        1819221647,
        1027324527,
        1763098305,
        992442602,
        608754025,
        920010930,
        2003060772,
        780309343,
        1431646620,
        2080999169,
        433243263,
        542575521,
        686870302,
        603251930,
        335981861,
        1798947269,
        179962615,
        1268672413,
        1544211620,
    ],
)
UPPER_LOWER_BOUNDED_SEQUENCE = (
    [
        30,
        33,
        19,
        19,
        61,
        50,
        4,
        15,
        48,
        37,
        29,
        29,
        52,
        38,
        57,
        19,
        62,
        8,
        15,
        32,
        40,
        19,
        4,
        11,
        27,
        61,
        34,
        27,
        8,
        12,
        40,
        39,
        14,
        62,
        29,
        20,
        22,
        63,
        6,
        62,
        54,
        31,
        19,
        60,
        38,
        6,
        54,
        12,
        25,
        25,
        10,
        12,
        18,
        29,
        26,
        8,
        55,
        8,
        47,
        35,
        16,
        25,
        45,
        7,
        56,
        16,
        47,
        4,
        26,
        36,
        15,
        19,
        40,
        18,
        36,
        21,
        27,
        14,
        4,
        48,
        43,
        19,
        6,
        47,
        17,
        50,
        37,
        4,
        42,
        12,
        18,
        46,
        25,
        27,
        61,
        9,
        39,
        58,
        45,
        34,
    ],
    [
        1302,
        2025,
        3451,
        2371,
        1213,
        3602,
        1276,
        3687,
        3960,
        3589,
        3641,
        1601,
        3724,
        2630,
        1329,
        2971,
        3194,
        3380,
        3267,
        4004,
        2872,
        1111,
        16,
        3083,
        1059,
        1873,
        1306,
        939,
        1220,
        264,
        1072,
        3051,
        1046,
        1334,
        2741,
        632,
        2314,
        2895,
        2838,
        3974,
        1266,
        763,
        1711,
        3612,
        1790,
        3738,
        1146,
        3024,
        1417,
        3877,
        502,
        2904,
        210,
        3221,
        3938,
        740,
        1567,
        1580,
        2399,
        2327,
        1528,
        1657,
        1377,
        2299,
        2048,
        208,
        1499,
        1216,
        2378,
        1548,
        2127,
        991,
        1012,
        150,
        4068,
        1413,
        1899,
        86,
        976,
        2400,
        475,
        2911,
        1758,
        1199,
        1409,
        3302,
        3709,
        1816,
        1074,
        3864,
        750,
        1078,
        1177,
        2979,
        1153,
        1581,
        2631,
        2650,
        4077,
        1906,
    ],
    [
        16137942,
        536745,
        12068251,
        2201731,
        11556013,
        12525362,
        13106476,
        15769047,
        15500040,
        1325749,
        9098201,
        3049601,
        5919964,
        14013590,
        16244049,
        16396651,
        16621274,
        14879300,
        13096227,
        6585284,
        582472,
        796951,
        6148816,
        219563,
        15639939,
        14763553,
        1723306,
        5680539,
        1608980,
        7128264,
        7781872,
        4625931,
        13077686,
        5240294,
        9774581,
        12828392,
        8187034,
        5082735,
        6151638,
        7495094,
        6023586,
        7226683,
        4290031,
        10085532,
        15473390,
        1941978,
        14571066,
        9885024,
        10829977,
        6613717,
        10531222,
        7196184,
        8462370,
        11231621,
        10085858,
        7655060,
        16599247,
        9565340,
        3225839,
        16583687,
        5852488,
        185497,
        5020017,
        1622299,
        16220288,
        13076848,
        8304539,
        10152496,
        3107498,
        7243788,
        8562207,
        12632911,
        6223252,
        3137910,
        11591508,
        10368933,
        1919739,
        9274166,
        6790336,
        16000320,
        6320635,
        3320191,
        11397438,
        12673919,
        7941329,
        10664582,
        10844509,
        7505176,
        14946354,
        5752824,
        12893790,
        11723158,
        637897,
        10052259,
        5272753,
        9630621,
        2601831,
        6241210,
        3166317,
        12654226,
    ],
)


def __bit_size_to_method(
    lib_pcg_exposer_client: (
        LibPcg32ExposerAlgopyClient
        | LibPcg32ExposerPytealClient
        | LibPcg32ExposerTsClient
    ),
    bit_size: int,
    lower_bound: int,
    upper_bound: int,
    length: int,
) -> SimulateAtomicTransactionResponse:
    match bit_size:
        case 8:
            result = (
                lib_pcg_exposer_client.compose()
                .bounded_rand_uint8(
                    seed=RNG_SEED,
                    lower_bound=lower_bound,
                    upper_bound=upper_bound,
                    length=length,
                )
                .simulate(SimulateOptions(extra_opcode_budget=320_000))
            )
        case 16:
            result = (
                lib_pcg_exposer_client.compose()
                .bounded_rand_uint16(
                    seed=RNG_SEED,
                    lower_bound=lower_bound,
                    upper_bound=upper_bound,
                    length=length,
                )
                .simulate(SimulateOptions(extra_opcode_budget=320_000))
            )
        case 32:
            result = (
                lib_pcg_exposer_client.compose()
                .bounded_rand_uint32(
                    seed=RNG_SEED,
                    lower_bound=lower_bound,
                    upper_bound=upper_bound,
                    length=length,
                )
                .simulate(SimulateOptions(extra_opcode_budget=320_000))
            )
        case _:
            raise ValueError("")

    return result


# This simple test ensures that the code size of this library doesn't grow unexpectedly if we
#  start taking subroutine inlining and opcode assembly opportunities.
def test_library_size(
    lib_pcg32_client: str, expected_library_size: int, request: pytest.FixtureRequest
):
    client = request.getfixturevalue(lib_pcg32_client)
    assert len(client.app_client.approval.teal.split("\n")) < expected_library_size


def test_unbounded_maximal_cost(
    lib_pcg32_client: str,
    bit_size: int,
    max_unbounded_opup_calls: int,
    request: pytest.FixtureRequest,
) -> None:
    expected_maximal_sequence_length = (1024 - 4 - 2) // (bit_size >> 3)

    client = request.getfixturevalue(lib_pcg32_client)
    result = __bit_size_to_method(
        client, bit_size, 0, 0, expected_maximal_sequence_length
    )

    assert result.abi_results[0].return_value
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < 700 * max_unbounded_opup_calls
    )


def test_bounded_maximal_cost(
    lib_pcg32_client: str,
    bit_size: int,
    max_bounded_opup_calls: int,
    request: pytest.FixtureRequest,
) -> None:
    expected_maximal_sequence_length = (1024 - 4 - 2) // (bit_size >> 3)

    client = request.getfixturevalue(lib_pcg32_client)
    result = __bit_size_to_method(
        client,
        bit_size,
        1,
        2**bit_size - 1,
        expected_maximal_sequence_length,
    )

    assert result.abi_results[0].return_value
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < 700 * max_bounded_opup_calls
    )


@pytest.mark.parametrize(
    "bit_size,expected_sequence", zip(BIT_SIZES, UNBOUNDED_SEQUENCE)
)
def test_unbounded_sequence(
    lib_pcg32_client: str,
    bit_size: int,
    expected_sequence: [int],
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg32_client)
    result = __bit_size_to_method(client, bit_size, 0, 0, 100)

    assert result.abi_results[0].return_value == expected_sequence


@pytest.mark.parametrize(
    "bit_size,expected_sequence", zip(BIT_SIZES, LOWER_BOUNDED_SEQUENCE)
)
def test_lower_bounded_sequence(
    lib_pcg32_client: str,
    bit_size: int,
    expected_sequence: [int],
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg32_client)
    result = __bit_size_to_method(client, bit_size, 2 ** (bit_size - 1) - 1, 0, 100)

    assert result.abi_results[0].return_value == expected_sequence


@pytest.mark.parametrize(
    "bit_size,expected_sequence", zip(BIT_SIZES, UPPER_BOUNDED_SEQUENCE)
)
def test_upper_bounded_sequence(
    lib_pcg32_client: str,
    bit_size: int,
    expected_sequence: [int],
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg32_client)
    result = __bit_size_to_method(client, bit_size, 0, 2 ** (bit_size - 1) + 1, 100)

    assert result.abi_results[0].return_value == expected_sequence


@pytest.mark.parametrize(
    "bit_size,expected_sequence", zip(BIT_SIZES, UPPER_LOWER_BOUNDED_SEQUENCE)
)
def test_upper_lower_bounded_sequence(
    lib_pcg32_client: str,
    bit_size: int,
    expected_sequence: [int],
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg32_client)
    result = __bit_size_to_method(
        client,
        bit_size,
        2 ** (bit_size >> 2),
        2 ** ((bit_size >> 2) * 3),
        100,
    )

    assert result.abi_results[0].return_value == expected_sequence
