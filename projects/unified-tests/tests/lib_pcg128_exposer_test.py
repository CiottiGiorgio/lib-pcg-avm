from collections.abc import Callable
from typing import Any

import algokit_utils
import pytest
from algokit_utils import (
    AlgorandClient,
    AppClientCompilationParams,
    SendAtomicTransactionComposerResults,
    SigningAccount,
)

from smart_contracts.artifacts.lib_pcg128_exposer_algo_py import (
    LibPcg128ExposerAlgoPyClient,
    LibPcg128ExposerAlgoPyFactory,
)
from smart_contracts.artifacts.lib_pcg128_exposer_algo_ts import (
    LibPcg128ExposerAlgoTsClient,
    LibPcg128ExposerAlgoTsFactory,
)
from smart_contracts.artifacts.lib_pcg128_exposer_pyteal import (
    LibPcg128ExposerPytealClient,
    LibPcg128ExposerPytealFactory,
)
from smart_contracts.artifacts.lib_pcg128_exposer_ts import (
    LibPcg128ExposerTsClient,
    LibPcg128ExposerTsFactory,
)


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    match metafunc.config.getoption("language"):
        case "algopy":
            if "lib_pcg128_client" in metafunc.fixturenames:
                metafunc.parametrize(
                    "lib_pcg128_client", ["lib_pcg128_exposer_algopy_client"]
                )
            if "get_random_sequence_method" in metafunc.fixturenames:

                def get_random_sequence_method(
                    client: LibPcg128ExposerAlgoPyClient,
                    seed: bytes,
                    lower_bound: int,
                    upper_bound: int,
                    length: int,
                ) -> SendAtomicTransactionComposerResults:
                    return (
                        client.new_group()
                        .bounded_rand_uint128((seed, lower_bound, upper_bound, length))
                        .simulate(extra_opcode_budget=320_000)
                    )

                metafunc.parametrize(
                    "get_random_sequence_method",
                    [get_random_sequence_method],
                )
            if "expected_library_size" in metafunc.fixturenames:
                metafunc.parametrize("expected_library_size", [11_000])
            if "max_unbounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize("max_unbounded_opup_calls", [19])
            if "max_bounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize("max_bounded_opup_calls", [23])
        case "algots":
            if "lib_pcg128_client" in metafunc.fixturenames:
                metafunc.parametrize(
                    "lib_pcg128_client", ["lib_pcg128_exposer_algots_client"]
                )
            if "get_random_sequence_method" in metafunc.fixturenames:

                def get_random_sequence_method(
                    client: LibPcg128ExposerAlgoTsClient,
                    seed: bytes,
                    lower_bound: int,
                    upper_bound: int,
                    length: int,
                ) -> SendAtomicTransactionComposerResults:
                    return (
                        client.new_group()
                        .bounded_rand_uint128((seed, lower_bound, upper_bound, length))
                        .simulate(extra_opcode_budget=320_000)
                    )

                metafunc.parametrize(
                    "get_random_sequence_method",
                    [get_random_sequence_method],
                )
            if "expected_library_size" in metafunc.fixturenames:
                metafunc.parametrize("expected_library_size", [12_000])
            if "max_unbounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize("max_unbounded_opup_calls", [21])
            if "max_bounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize("max_bounded_opup_calls", [26])
        case "ts":
            if "lib_pcg128_client" in metafunc.fixturenames:
                metafunc.parametrize(
                    "lib_pcg128_client", ["lib_pcg128_exposer_ts_client"]
                )
            if "get_random_sequence_method" in metafunc.fixturenames:

                def get_random_sequence_method(
                    client: LibPcg128ExposerTsClient,
                    seed: bytes,
                    lower_bound: int,
                    upper_bound: int,
                    length: int,
                ) -> SendAtomicTransactionComposerResults:
                    return (
                        client.new_group()
                        .bounded_rand_uint128((seed, lower_bound, upper_bound, length))
                        .simulate(extra_opcode_budget=320_000)
                    )

                metafunc.parametrize(
                    "get_random_sequence_method",
                    [get_random_sequence_method],
                )
            if "expected_library_size" in metafunc.fixturenames:
                metafunc.parametrize("expected_library_size", [29_500])
            if "max_unbounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize("max_unbounded_opup_calls", [44])
            if "max_bounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize("max_bounded_opup_calls", [50])
        case "pyteal":
            if "lib_pcg128_client" in metafunc.fixturenames:
                metafunc.parametrize(
                    "lib_pcg128_client", ["lib_pcg128_exposer_pyteal_client"]
                )
            if "get_random_sequence_method" in metafunc.fixturenames:

                def get_random_sequence_method(
                    client: LibPcg128ExposerPytealClient,
                    seed: bytes,
                    lower_bound: int,
                    upper_bound: int,
                    length: int,
                ) -> SendAtomicTransactionComposerResults:
                    result = (
                        client.new_group()
                        .bounded_rand_uint128(
                            (
                                seed,
                                lower_bound.to_bytes(16, "big"),
                                upper_bound.to_bytes(16, "big"),
                                length,
                            )
                        )
                        .simulate(extra_opcode_budget=320_000)
                    )
                    result.returns[0].value = [
                        int.from_bytes(x, "big") for x in result.returns[0].value
                    ]
                    return result

                metafunc.parametrize(
                    "get_random_sequence_method",
                    [get_random_sequence_method],
                )
            if "expected_library_size" in metafunc.fixturenames:
                metafunc.parametrize("expected_library_size", [10_500])
            if "max_unbounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize("max_unbounded_opup_calls", [21])
            if "max_bounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize("max_bounded_opup_calls", [24])
        case _:
            raise ValueError


@pytest.fixture(scope="session")
def lib_pcg128_exposer_algopy_client(
    algorand_client: AlgorandClient, deployer: SigningAccount
) -> LibPcg128ExposerAlgoPyClient:
    client, _ = LibPcg128ExposerAlgoPyFactory(
        algorand_client, default_sender=deployer.address
    ).deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.UpdateApp,
    )

    return client


@pytest.fixture(scope="session")
def lib_pcg128_exposer_algots_client(
    algorand_client: AlgorandClient, deployer: SigningAccount
) -> LibPcg128ExposerAlgoTsClient:
    client, _ = LibPcg128ExposerAlgoTsFactory(
        algorand_client, default_sender=deployer.address
    ).deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.UpdateApp,
    )

    return client


@pytest.fixture(scope="session")
def lib_pcg128_exposer_ts_client(
    algorand_client: AlgorandClient, deployer: SigningAccount
) -> LibPcg128ExposerTsClient:
    client, _ = LibPcg128ExposerTsFactory(
        algorand_client, default_sender=deployer.address
    ).deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
    )

    return client


@pytest.fixture(scope="session")
def lib_pcg128_exposer_pyteal_client(
    algorand_client: AlgorandClient, deployer: SigningAccount
) -> LibPcg128ExposerPytealClient:
    client, _ = LibPcg128ExposerPytealFactory(
        algorand_client, default_sender=deployer.address
    ).deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.UpdateApp,
        compilation_params=AppClientCompilationParams(updatable=True, deletable=True),
    )

    return client


RNG_SEED = (
    b"\x00\x00\x00\x00\x00\x00\x00\x2a"
    + b"\x00\x00\x00\x00\x00\x00\x00\x36"
    + b"\x00\x00\x00\x00\x00\x00\x00\x2a"
    + b"\x00\x00\x00\x00\x00\x00\x00\x36"
)

EXPECTED_MAXIMAL_SEQUENCE_LENGTH = 63
UNBOUNDED_SEQUENCE = [
    259144855606245380863112797115970883539,
    142267730433529068318787069226796711920,
    152485804416160131467158683808138918400,
    90560543349351729472161848464000272168,
    326571431199454864426323003959162081959,
    139229943393974074601651802638302609275,
    270867547594701782853700928754605750662,
    284370575307897106345909187452677854172,
    163391360514882350029044459477868677489,
    339052983354591731389745619006002826878,
    241307409648011125834748877948089547264,
    137149988509448207446390195171452995873,
    8444253889468935977777103010250226970,
    330753763641954673782584210963898272052,
    304346324591310041915675804470203217953,
    19907964238602532945707477105196201030,
    239245033488307529490520423929836152800,
    58334771022693378433862610382322472707,
    35596970338870227912590368062972433183,
    257058808353903543699917467426574661876,
    93090667907668903468346888810160856868,
    288501194552846071134443107961239207513,
    227781658134979739518269275823667809035,
    320356434282817439336121728601383493602,
    162073236681816478347790941942529761348,
    217830526220037603883831505275246168575,
    62609276635075465190524192772635493749,
    191855949122385203511996787231161125974,
    176912082171149701042947152414726212897,
    52403839819015132807066267678950076979,
    293042220142118169974855281376724666887,
    106703100854897323232065986420036537819,
    196429634660408820915035068143412550189,
    158590876491926555063562348973128601641,
    301175345103290750037878556148145081805,
    246919776663297136710021868326063283070,
    174774833882986450738399148352259701471,
    239660063916576996494337728229664955265,
    8462608989478692118804279759921066141,
    69712603373457784787199396329824969829,
    286256875767254274007149562371182336034,
    172040331635309576623032325994924393189,
    17619571274783574664847621188033367973,
    148341094148214630707223708378821243986,
    10530361977951058642527698445515987451,
    183584503521630451288209756380758929581,
    224461314408368065120348383379747166065,
    150983623668889236287684826786353163278,
    257395107607906528567083687416399278257,
    213197206522083889655641270226920160779,
    170972936429123391099972254178225595697,
    294325024838211405406093063797108367943,
    170809025088488880750869165864378487878,
    189637335771469783769410838020016104601,
    36687672051956526087683414088605148844,
    89663392891602718918013837037461173661,
    198037849208039204697579025440875841286,
    257294912760209694549121406261915180509,
    300656500280625713758562554119116237501,
    77078714428859089355418704090814160597,
    112117109527134587993146266905079829032,
    33244869168026131474505847284776822330,
    64199676694185550255014131541788428619,
]
LOWER_BOUNDED_SEQUENCE = [
    259144855606245380863112797115970883537,
    326571431199454864426323003959162081957,
    270867547594701782853700928754605750660,
    284370575307897106345909187452677854170,
    339052983354591731389745619006002826876,
    241307409648011125834748877948089547262,
    330753763641954673782584210963898272050,
    304346324591310041915675804470203217951,
    239245033488307529490520423929836152798,
    257058808353903543699917467426574661874,
    288501194552846071134443107961239207511,
    227781658134979739518269275823667809033,
    320356434282817439336121728601383493600,
    217830526220037603883831505275246168573,
    191855949122385203511996787231161125972,
    176912082171149701042947152414726212895,
    293042220142118169974855281376724666885,
    196429634660408820915035068143412550187,
    301175345103290750037878556148145081803,
    246919776663297136710021868326063283068,
    174774833882986450738399148352259701469,
    239660063916576996494337728229664955263,
    286256875767254274007149562371182336032,
    172040331635309576623032325994924393187,
    183584503521630451288209756380758929579,
    224461314408368065120348383379747166063,
    257395107607906528567083687416399278255,
    213197206522083889655641270226920160777,
    170972936429123391099972254178225595695,
    294325024838211405406093063797108367941,
    170809025088488880750869165864378487876,
    189637335771469783769410838020016104599,
    198037849208039204697579025440875841284,
    257294912760209694549121406261915180507,
    300656500280625713758562554119116237499,
    255163756631692085050150554348586151275,
    294412837776159748024061504516575840022,
    206601087346427921990797519155375228620,
    195886570405508926119392391077649484397,
    338537112816821381868190044208626937605,
    286601149647428527933877797483228662849,
    239992143307707234054776600589722810080,
    308914155110952590100639814007695363051,
    174626962508238153748080265196691334517,
    304651598758626514820570436954121161948,
    215006552942748269382737767306212238051,
    305017723038326059097819113678389540107,
    202884487412063436490962940728133669035,
    210873989024345002202890099663775621832,
    339542567961649449115567845136607413116,
    239713153844281825976856526193854959160,
    276167527707375790313406466360308709169,
    234736959320434316263054145521093190868,
    201128095009033395208225418776187959337,
    231488260144052069963280002061917152999,
    305968615314637303456714092372952549995,
    254881224066244015472925634726574642448,
    301026013581602137135899884975299300621,
    199557580199173387508832933582900818164,
    174942876225027204219040802296746374483,
    332504509584492969573431532673035033957,
    221184980803478878411799438458308045679,
    311662366111754446272097487017993246723,
]
UPPER_BOUNDED_SEQUENCE = [
    89003672145776149131425493400086777810,
    156430247738985632694635700243277976230,
    100726364134232551122013625038721644933,
    114229391847427874614221883736793748443,
    168911799894122499658058315290118721149,
    71166226187541894103061574232205441535,
    160612580181485442050896907248014166323,
    134205141130840810183988500754319112224,
    69103850027838297758833120213952047071,
    86917624893434311968230163710690556147,
    118360011092376839402755804245355101784,
    57640474674510507786581972107783703306,
    150215250822348207604434424885499387873,
    47689342759568372152144201559362062846,
    21714765661915971780309483515277020245,
    6770898710680469311259848698842107168,
    122901036681648938243167977660840561158,
    26288451199939589183347764427528444460,
    131034161642821518306191252432260976076,
    76778593202827904978334564610179177341,
    4633650422517219006711844636375595742,
    69518880456107764762650424513780849536,
    116115692306785042275462258655298230305,
    1899148174840344891345022279040287460,
    13443320061161219556522452664874823852,
    54320130947898833388661079663863060336,
    87253924147437296835396383700515172528,
    43056023061614657923953966511036055050,
    831752968654159368284950462341489968,
    124183841377742173674405760081224262214,
    667841628019649019181862148494382149,
    19496152311000552037723534304131998872,
    27896665747569972965891721724991735557,
    87153729299740462817434102546031074780,
    130515316820156482026875250403232131772,
    85022573171222853318463250632702045548,
    124271654315690516292374200800691734295,
    36459903885958690259110215439491122893,
    25745386945039694387705087361765378670,
    168395929356352150136502740492742831878,
    116459966186959296202190493767344557122,
    69850959847238002323089296873838704353,
    138772971650483358368952510291811257324,
    4485779047768922016392961480807228790,
    134510415298157283088883133238237056221,
    44865369482279037651050463590328132324,
    134876539577856827366131809962505434380,
    32743303951594204759275637012249563308,
    40732805563875770471202795947891516105,
    169401384501180217383880541420723307389,
    69571970383812594245169222477970853433,
    106026344246906558581719162644424603442,
    64595775859965084531366841805209085141,
    30986911548564163476538115060303853610,
    61347076683582838231592698346033047272,
    135827431854168071725026788657068444268,
    84740040605774783741238331010690536721,
    130884830121132905404212581259415194894,
    29416396738704155777145629867016712437,
    4801692764557972487353498580862268756,
    162363326124023737841744228957150928230,
    51043797343009646680112134742423939952,
    141521182651285214540410183302109140996,
]
UPPER_LOWER_BOUNDED_SEQUENCE = [
    2422641556802136066611875795,
    64691545494316202453634383856,
    22293208800062080522037623296,
    20759408350597346505169684264,
    28932022522850655369773879975,
    69265216260548706345342500731,
    51405700411352658396342253958,
    22954134380348306655364977628,
    77406264895826172065487456625,
    69071595213983144889817763454,
    62073775145700340164381391360,
    30568989280267465029775739169,
    21756071937467365384634891546,
    21358577007648308771009300788,
    70086786043811455949906999329,
    3640090635922230371180409926,
    78870129090813975268547831776,
    31466063217304276245391415043,
    72442017310992861392524350239,
    3923303953354773007547332852,
    67530643061480163333353119524,
    69469017315999565031892549209,
    36892644564154671336830667531,
    68730678267158328119790133218,
    17008122369169582805172985924,
    45899360682196919720024033791,
    21015587629058686247073744245,
    11689230690451282189929483350,
    45720578246266785177162272033,
    21150979869323662096536482355,
    62477881721749523996004993543,
    54234175849381707654487281115,
    44929008528000282899525245485,
    18019480074351988313004363817,
    70902951283911704304664202701,
    45101290932631645815049132926,
    52968345801105124721819073247,
    36833460989052668321391254401,
    16443498402347890465408921757,
    34859465387401680502426952805,
    23445102644932888320369924130,
    77140832398929128451600728805,
    10054887490968454595572060069,
    77625764376771703102632309842,
    9166884087458725646349998587,
    9663842389834211317826842797,
    58671144012456706501009659761,
    51959155628711513408250096654,
    31099128586606270963804942513,
    19144185129491679102149082635,
    31403234537157544008238671153,
    29242459383179951856264667719,
    33242684991404648631451833414,
    60698427882554382792518329497,
    76512906684608790671479449260,
    40129959391769420129700803997,
    71972184854437780340522452742,
    49159846277739844875485601245,
    43677903471268595839326694077,
    154203591051069988387888853,
    15641183202696225200628945448,
    29591021105313311755635516986,
    11879797573749107793597139275,
]


# This simple test ensures that the code size of this library doesn't grow unexpectedly if we
#  start taking subroutine inlining and opcode assembly opportunities.
def test_library_size(
    lib_pcg128_client: str,
    expected_library_size: int,
    request: pytest.FixtureRequest,
):
    client = request.getfixturevalue(lib_pcg128_client)
    assert len(client.app_client.app_spec.source.approval) < expected_library_size


def test_unbounded_maximal_cost(
    lib_pcg128_client: str,
    get_random_sequence_method: Callable[[Any, bytes, int, int, int], Any],
    max_unbounded_opup_calls: int,
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg128_client)
    result = get_random_sequence_method(
        client, RNG_SEED, 0, 0, EXPECTED_MAXIMAL_SEQUENCE_LENGTH
    )

    assert result.returns[0].value
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < 700 * max_unbounded_opup_calls
    )


def test_bounded_maximal_cost(
    lib_pcg128_client: str,
    get_random_sequence_method: Callable[[Any, bytes, int, int, int], Any],
    max_bounded_opup_calls: int,
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg128_client)
    result = get_random_sequence_method(
        client, RNG_SEED, 1, 2**64 - 1, EXPECTED_MAXIMAL_SEQUENCE_LENGTH
    )

    assert result.returns[0].value
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < 700 * max_bounded_opup_calls
    )


def test_unbounded_sequence(
    lib_pcg128_client: str,
    get_random_sequence_method: Callable[[Any, bytes, int, int, int], Any],
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg128_client)
    result = get_random_sequence_method(
        client, RNG_SEED, 0, 0, EXPECTED_MAXIMAL_SEQUENCE_LENGTH
    )

    assert result.returns[0].value == UNBOUNDED_SEQUENCE


def test_lower_bounded_sequence(
    lib_pcg128_client: str,
    get_random_sequence_method: Callable[[Any, bytes, int, int, int], Any],
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg128_client)
    result = get_random_sequence_method(
        client, RNG_SEED, 2**127 - 1, 0, EXPECTED_MAXIMAL_SEQUENCE_LENGTH
    )

    assert result.returns[0].value == LOWER_BOUNDED_SEQUENCE


def test_upper_bounded_sequence(
    lib_pcg128_client: str,
    get_random_sequence_method: Callable[[Any, bytes, int, int, int], Any],
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg128_client)
    result = get_random_sequence_method(
        client, RNG_SEED, 0, 2**127 + 1, EXPECTED_MAXIMAL_SEQUENCE_LENGTH
    )

    assert result.returns[0].value == UPPER_BOUNDED_SEQUENCE


def test_upper_lower_bounded_sequence(
    lib_pcg128_client: str,
    get_random_sequence_method: Callable[[Any, bytes, int, int, int], Any],
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg128_client)
    result = get_random_sequence_method(
        client, RNG_SEED, 2**32, 2**96, EXPECTED_MAXIMAL_SEQUENCE_LENGTH
    )

    assert result.returns[0].value == UPPER_LOWER_BOUNDED_SEQUENCE
