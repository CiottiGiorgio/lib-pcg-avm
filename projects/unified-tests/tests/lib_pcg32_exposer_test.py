import algokit_utils
import pytest
from algokit_utils import (
    AlgorandClient,
    AppClientCompilationParams,
    SendAtomicTransactionComposerResults,
    SigningAccount,
)

from smart_contracts.artifacts.lib_pcg32_exposer_algo_py import (
    LibPcg32ExposerAlgoPyClient,
    LibPcg32ExposerAlgoPyFactory,
)
from smart_contracts.artifacts.lib_pcg32_exposer_algo_ts import (
    LibPcg32ExposerAlgoTsClient,
    LibPcg32ExposerAlgoTsFactory,
)
from smart_contracts.artifacts.lib_pcg32_exposer_pyteal import (
    LibPcg32ExposerPytealClient,
    LibPcg32ExposerPytealFactory,
)
from smart_contracts.artifacts.lib_pcg32_exposer_ts import (
    LibPcg32ExposerTsClient,
    LibPcg32ExposerTsFactory,
)


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    match metafunc.config.getoption("language"):
        case "algopy":
            if "lib_pcg32_client" in metafunc.fixturenames:
                metafunc.parametrize(
                    "lib_pcg32_client", ["lib_pcg32_exposer_algopy_client"]
                )
            if "expected_library_size" in metafunc.fixturenames:
                metafunc.parametrize("expected_library_size", [6_500])
            if "max_unbounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize(
                    "max_unbounded_opup_calls",
                    [12],
                )
            if "max_bounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize(
                    "max_bounded_opup_calls",
                    [14],
                )
        case "algots":
            if "lib_pcg32_client" in metafunc.fixturenames:
                metafunc.parametrize(
                    "lib_pcg32_client", ["lib_pcg32_exposer_algots_client"]
                )
            if "expected_library_size" in metafunc.fixturenames:
                metafunc.parametrize("expected_library_size", [13_500])
        case "ts":
            if "lib_pcg32_client" in metafunc.fixturenames:
                metafunc.parametrize(
                    "lib_pcg32_client", ["lib_pcg32_exposer_ts_client"]
                )
            if "expected_library_size" in metafunc.fixturenames:
                metafunc.parametrize("expected_library_size", [35_500])
        case "pyteal":
            if "lib_pcg32_client" in metafunc.fixturenames:
                metafunc.parametrize(
                    "lib_pcg32_client", ["lib_pcg32_exposer_pyteal_client"]
                )
            if "expected_library_size" in metafunc.fixturenames:
                metafunc.parametrize("expected_library_size", [9_500])
        case _:
            raise ValueError


@pytest.fixture(scope="session")
def lib_pcg32_exposer_algopy_client(
    algorand_client: AlgorandClient, deployer: SigningAccount
) -> LibPcg32ExposerAlgoPyClient:
    client, _ = LibPcg32ExposerAlgoPyFactory(
        algorand_client, default_sender=deployer.address
    ).deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.UpdateApp,
    )

    return client


@pytest.fixture(scope="session")
def lib_pcg32_exposer_algots_client(
    algorand_client: AlgorandClient, deployer: SigningAccount
) -> LibPcg32ExposerAlgoTsClient:
    client, _ = LibPcg32ExposerAlgoTsFactory(
        algorand_client, default_sender=deployer.address
    ).deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
    )

    return client


@pytest.fixture(scope="session")
def lib_pcg32_exposer_ts_client(
    algorand_client: AlgorandClient,
    deployer: SigningAccount,
) -> LibPcg32ExposerTsClient:
    client, _ = LibPcg32ExposerTsFactory(
        algorand_client, default_sender=deployer.address
    ).deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.UpdateApp,
    )

    return client


@pytest.fixture(scope="session")
def lib_pcg32_exposer_pyteal_client(
    algorand_client: AlgorandClient, deployer: SigningAccount
) -> LibPcg32ExposerPytealClient:
    client, _ = LibPcg32ExposerPytealFactory(
        algorand_client, default_sender=deployer.address
    ).deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.UpdateApp,
        compilation_params=AppClientCompilationParams(updatable=True, deletable=True),
    )

    return client


RNG_SEED = b"\x00\x00\x00\x00\x00\x00\x00\x2a"

UNBOUNDED_SEQUENCE = [
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
    ]
LOWER_BOUNDED_SEQUENCE = [
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
    ]
UPPER_BOUNDED_SEQUENCE = [
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
    ]
UPPER_LOWER_BOUNDED_SEQUENCE = [
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
    ]


# This simple test ensures that the code size of this library doesn't grow unexpectedly if we
#  start taking subroutine inlining and opcode assembly opportunities.
def test_library_size(
    lib_pcg32_client: str, expected_library_size: int, request: pytest.FixtureRequest
) -> None:
    client = request.getfixturevalue(lib_pcg32_client)
    assert len(client.app_client.app_spec.source.approval) < expected_library_size


def test_unbounded_maximal_cost(
    lib_pcg32_client: str,
    max_unbounded_opup_calls: int,
    request: pytest.FixtureRequest,
) -> None:
    expected_maximal_sequence_length = (1024 - 4 - 2) // (64 >> 3)

    client = request.getfixturevalue(lib_pcg32_client)
    result = (
        client.new_group()
        .bounded_rand_uint32((RNG_SEED, 0, 0, expected_maximal_sequence_length))
        .simulate(extra_opcode_budget=320_000)
    )

    assert result.returns[0].value
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < 700 * max_unbounded_opup_calls
    )


def test_bounded_maximal_cost(
    lib_pcg32_client: str,
    max_bounded_opup_calls: int,
    request: pytest.FixtureRequest,
) -> None:
    expected_maximal_sequence_length = (1024 - 4 - 2) // (64 >> 3)

    client = request.getfixturevalue(lib_pcg32_client)
    result = (
        client.new_group()
        .bounded_rand_uint32((RNG_SEED, 1, 2**32-1, expected_maximal_sequence_length))
        .simulate(extra_opcode_budget=320_000)
    )

    assert result.returns[0].value
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < 700 * max_bounded_opup_calls
    )


def test_unbounded_sequence(
    lib_pcg32_client: str,
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg32_client)
    result = (
        client.new_group()
        .bounded_rand_uint32((RNG_SEED, 0, 0, 100))
        .simulate(extra_opcode_budget=320_000)
    )

    assert result.returns[0].value == UNBOUNDED_SEQUENCE


def test_lower_bounded_sequence(
    lib_pcg32_client: str,
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg32_client)
    result = (
        client.new_group()
        .bounded_rand_uint32((RNG_SEED, 2**31-1, 0, 100))
        .simulate(extra_opcode_budget=320_000)
    )

    assert result.returns[0].value == LOWER_BOUNDED_SEQUENCE


def test_upper_bounded_sequence(
    lib_pcg32_client: str,
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg32_client)
    result = (
        client.new_group()
        .bounded_rand_uint32((RNG_SEED, 0, 2**31+1, 100))
        .simulate(extra_opcode_budget=320_000)
    )

    assert result.returns[0].value == UPPER_BOUNDED_SEQUENCE


def test_upper_lower_bounded_sequence(
    lib_pcg32_client: str,
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg32_client)
    result = (
        client.new_group()
        .bounded_rand_uint32((RNG_SEED, 2**8, 2**24, 100))
        .simulate(extra_opcode_budget=320_000)
    )

    assert result.returns[0].value == UPPER_LOWER_BOUNDED_SEQUENCE
