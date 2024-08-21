import algokit_utils
import pytest
from algokit_utils import get_localnet_default_account
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.lib_pcg64_exposer_algopy import (
    LibPcg64ExposerAlgopyClient,
    SimulateOptions,
)
from smart_contracts.artifacts.lib_pcg64_exposer_pyteal import (
    LibPcg64ExposerPytealClient,
)
from smart_contracts.artifacts.lib_pcg64_exposer_ts import (
    CreateApplicationArgs as CreateApplicationArgsTs,
)
from smart_contracts.artifacts.lib_pcg64_exposer_ts import (
    Deploy as DeployTs,
)
from smart_contracts.artifacts.lib_pcg64_exposer_ts import (
    DeployCreate as DeployCreateTs,
)
from smart_contracts.artifacts.lib_pcg64_exposer_ts import (
    LibPcg64ExposerTsClient,
)
from smart_contracts.artifacts.lib_pcg64_exposer_ts import (
    UpdateApplicationArgs as UpdateApplicationArgsTs,
)


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    match metafunc.config.getoption("language"):
        case "algopy":
            if "lib_pcg64_client" in metafunc.fixturenames:
                metafunc.parametrize(
                    "lib_pcg64_client", ["lib_pcg64_exposer_algopy_client"]
                )
            if "expected_library_size" in metafunc.fixturenames:
                metafunc.parametrize("expected_library_size", [350])
            if "max_unbounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize("max_unbounded_opup_calls", [23])
            if "max_bounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize("max_bounded_opup_calls", [25])
        case "ts":
            if "lib_pcg64_client" in metafunc.fixturenames:
                metafunc.parametrize(
                    "lib_pcg64_client", ["lib_pcg64_exposer_ts_client"]
                )
            if "expected_library_size" in metafunc.fixturenames:
                metafunc.parametrize("expected_library_size", [2000])
            if "max_unbounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize("max_unbounded_opup_calls", [40])
            if "max_bounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize("max_bounded_opup_calls", [42])
        case "pyteal":
            if "lib_pcg64_client" in metafunc.fixturenames:
                metafunc.parametrize(
                    "lib_pcg64_client", ["lib_pcg64_exposer_pyteal_client"]
                )
            if "expected_library_size" in metafunc.fixturenames:
                metafunc.parametrize("expected_library_size", [450])
            if "max_unbounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize("max_unbounded_opup_calls", [21])
            if "max_bounded_opup_calls" in metafunc.fixturenames:
                metafunc.parametrize("max_bounded_opup_calls", [23])


@pytest.fixture(scope="session")
def lib_pcg64_exposer_algopy_client(
    algod_client: AlgodClient, indexer_client: IndexerClient
) -> LibPcg64ExposerAlgopyClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = LibPcg64ExposerAlgopyClient(
        algod_client,
        creator=get_localnet_default_account(algod_client),
        indexer_client=indexer_client,
    )

    client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.ReplaceApp,
        on_update=algokit_utils.OnUpdate.UpdateApp,
    )
    return client


@pytest.fixture(scope="session")
def lib_pcg64_exposer_pyteal_client(
    algod_client: AlgodClient, indexer_client: IndexerClient
) -> LibPcg64ExposerPytealClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = LibPcg64ExposerPytealClient(
        algod_client,
        creator=get_localnet_default_account(algod_client),
        indexer_client=indexer_client,
    )

    client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.ReplaceApp,
        on_update=algokit_utils.OnUpdate.UpdateApp,
        allow_update=True,
        allow_delete=True,
    )
    return client


@pytest.fixture(scope="session")
def lib_pcg64_exposer_ts_client(
    algod_client: AlgodClient, indexer_client: IndexerClient
) -> LibPcg64ExposerTsClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = LibPcg64ExposerTsClient(
        algod_client,
        creator=get_localnet_default_account(algod_client),
        indexer_client=indexer_client,
    )

    client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.ReplaceApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
        create_args=DeployCreateTs(args=CreateApplicationArgsTs()),
        update_args=DeployTs(args=UpdateApplicationArgsTs()),
    )
    return client


RNG_SEED = b"\x00\x00\x00\x00\x00\x00\x00\x2A" + b"\x00\x00\x00\x00\x00\x00\x00\x36"

EXPECTED_MAXIMAL_SEQUENCE_LENGTH = 127
# These sequences WERE NOT generated using the reference C implementation.
UNBOUNDED_SEQUENCE = [
    14048270771836679757,
    7712349120530716571,
    8266272021060027030,
    4909296892041742261,
    17703472758907470354,
    7547670355139024912,
    14683759177899822202,
    15415759776988739333,
    8857463401779885611,
    18380099057036996406,
    13081300888861161772,
    7434915774915285829,
    457763920599069550,
    17930197454918215322,
    16498647315493842491,
    1079212903862829868,
    12969499253219514232,
    3162334273712430608,
    1929715628765258203,
    13935185923691857900,
    5046455219181062631,
    15639681094942944413,
    12348068430114775388,
    17366557100957019965,
    8786007765609138688,
    11808616488071270319,
    3394055687274737607,
    10400531842137922272,
    9590423191444729096,
    2840817848917929524,
    15885850585402998289,
    5784386687890978163,
    10648471831967459232,
    8597228641446354259,
    16326748173002968049,
    13385547914399115735,
    9474562729586353027,
    12991998097818381504,
    458758952564407866,
    3779127801356161773,
    15518016329788511640,
    9326325065706464935,
    955158872719177023,
    8041586827218552574,
    570852066677664566,
    9952135877641223737,
    12168072236025225729,
    8184838639577176878,
    13953416742781622434,
    11557443723954205410,
    9268461455634081170,
    15955391567321942946,
    9259575804053533787,
    10280260571389530128,
    1988842687108349494,
    4860662268274850161,
    10735653317285641974,
    13947985169204384349,
    16298621538807153618,
    4178445481807941089,
    6077880686105728352,
    1802207968798514804,
    3480271447235149052,
    5411203712988244988,
    13832454963982154894,
    4163383724275780270,
    15960151916226739339,
    2853806828365885435,
    7218994957810933071,
    11199867386943230672,
    6017462347003429409,
    6827567329366980652,
    10619032259719374847,
    9164650928465863583,
    18352133659148402485,
    15536679454229258657,
    1665543493686409777,
    13010000157683434860,
    16746269904140944560,
    68719752109543391,
    9466546606298826939,
    16515196261264253656,
    7542825957178955193,
    11655528589957365005,
    16535043898236750475,
    10998390100788357753,
    11431501851043963447,
    18406639491766368385,
    7846294412490071119,
    12994876108566115229,
    14971071675514378575,
    4589908637609925222,
    1732094517713878114,
    12725116062892818212,
    10903175877833247431,
    1698661479174571475,
    12549003727653543192,
    2188499530732965513,
    16586591871825567360,
    13817138842919319894,
    16318652894991200033,
    1515637311666843341,
    10818038099394703468,
    9483672323201859883,
    7706378835911928086,
    6765338338404978746,
    18025105582636725443,
    11990461835414819702,
    16895250721016841301,
    249034396698903878,
    1942539213530368147,
    635182335254356424,
    17864317628199680692,
    18224881932436611675,
    2882736064085953632,
    2927826973340545023,
    15102923566793133081,
    9539333478657395715,
    6277915296348610525,
    7537871472150270787,
    6418928171370148786,
    9445724195982350142,
    12520863958422770157,
    8727319097709596648,
    378448003553033351,
    11829701322416188382,
    2605198304164840470,
]
LOWER_BOUNDED_SEQUENCE = [
    14048270771836679755,
    17703472758907470352,
    14683759177899822200,
    15415759776988739331,
    18380099057036996404,
    13081300888861161770,
    17930197454918215320,
    16498647315493842489,
    12969499253219514230,
    13935185923691857898,
    15639681094942944411,
    12348068430114775386,
    17366557100957019963,
    11808616488071270317,
    10400531842137922270,
    9590423191444729094,
    15885850585402998287,
    10648471831967459230,
    16326748173002968047,
    13385547914399115733,
    9474562729586353025,
    12991998097818381502,
    15518016329788511638,
    9326325065706464933,
    9952135877641223735,
    12168072236025225727,
    13953416742781622432,
    11557443723954205408,
    9268461455634081168,
    15955391567321942944,
    9259575804053533785,
    10280260571389530126,
    10735653317285641972,
    13947985169204384347,
    16298621538807153616,
    13832454963982154892,
    15960151916226739337,
    11199867386943230670,
    10619032259719374845,
    18352133659148402483,
    15536679454229258655,
    13010000157683434858,
    16746269904140944558,
    9466546606298826937,
    16515196261264253654,
    11655528589957365003,
    16535043898236750473,
    10998390100788357751,
    11431501851043963445,
    18406639491766368383,
    12994876108566115227,
    14971071675514378573,
    12725116062892818210,
    10903175877833247429,
    12549003727653543190,
    16586591871825567358,
    13817138842919319892,
    16318652894991200031,
    10818038099394703466,
    9483672323201859881,
    18025105582636725441,
    11990461835414819700,
    16895250721016841299,
    17864317628199680690,
    18224881932436611673,
    15102923566793133079,
    9539333478657395713,
    9445724195982350140,
    12520863958422770155,
    11829701322416188380,
    15244572036978279514,
    15204276443289332059,
    17520215145058845268,
    12818048997932234705,
    10857162122855097677,
    11057895448646740158,
    12898076259823057623,
    16764247759469818902,
    13597544016353148519,
    16590742698129821942,
    14608127200177485471,
    17036869519386771727,
    13635697290629213735,
    16795821605013781237,
    13485880563821517916,
    11837950670804688225,
    13174788898569943146,
    17826452549728959091,
    12574775152811025531,
    15372247455199486572,
    18161195416760204539,
    11084137688641389636,
    11553716161079585695,
    12173457528097282819,
    11814319352728697292,
    10666403146990404965,
    16949791731578793700,
    9996305589648788389,
    14672278566164787644,
    15855710451318706613,
    13070411055694834119,
    17488750696827476801,
    15387169047177408893,
    16193100090511567301,
    15179625156539087633,
    13859767476273869037,
    10583178977711562571,
    17922719039953673563,
    13022414521982040442,
    12513591690395604260,
    17743368490578104206,
    17429588722904888176,
    11388657758044607901,
    12041052815950668460,
    18362943322664363322,
    13137021908211906357,
    17930510688199976111,
    9686480053674889349,
    13938646471129374891,
    15067301909135414152,
    15872388857307943825,
    12299998356978671345,
    9579966494188634068,
    13039355389449053211,
    11735712420227277298,
    16690561696084350850,
    11506937599907049698,
]
UPPER_BOUNDED_SEQUENCE = [
    4824898734981903948,
    8480100722052694545,
    5460387141045046393,
    6192387740133963524,
    9156727020182220597,
    3857928852006385963,
    8706825418063439513,
    7275275278639066682,
    3746127216364738423,
    4711813886837082091,
    6416309058088168604,
    3124696393259999579,
    8143185064102244156,
    2585244451216494510,
    1177159805283146463,
    367051154589953287,
    6662478548548222480,
    1425099795112683423,
    7103376136148192240,
    4162175877544339926,
    251190692731577218,
    3768626060963605695,
    6294644292933735831,
    102953028851689126,
    728763840786447928,
    2944700199170449920,
    4730044705926846625,
    2334071687099429601,
    45089418779305361,
    6732019530467167137,
    36203767198757978,
    1056888534534754319,
    1512281280430866165,
    4724613132349608540,
    7075249501952377809,
    4609082927127379085,
    6736779879371963530,
    1976495350088454863,
    1395660222864599038,
    9128761622293626676,
    6313307417374482848,
    3786628120828659051,
    7522897867286168751,
    243174569444051130,
    7291824224409477847,
    2432156553102589196,
    7311671861381974666,
    1775018063933581944,
    2208129814189187638,
    9183267454911592576,
    3771504071711339420,
    5747699638659602766,
    3501744026038042403,
    1679803840978471622,
    3325631690798767383,
    7363219834970791551,
    4593766806064544085,
    7095280858136424224,
    1594666062539927659,
    260300286347084074,
    8801733545781949634,
    2767089798560043893,
    7671878684162065492,
    8640945591344904883,
    9001509895581835866,
    5879551529938357272,
    315961441802619906,
    222352159127574333,
    3297491921567994348,
    2606329285561412573,
    6021200000123503707,
    5980904406434556252,
    8296843108204069461,
    3594676961077458898,
    1633790086000321870,
    1834523411791964351,
    3674704222968281816,
    7540875722615043095,
    4374171979498372712,
    7367370661275046135,
    5384755163322709664,
    7813497482531995920,
    4412325253774437928,
    7572449568159005430,
    4262508526966742109,
    2614578633949912418,
    3951416861715167339,
    8603080512874183284,
    3351403115956249724,
    6148875418344710765,
    8937823379905428732,
    1860765651786613829,
    2330344124224809888,
    2950085491242507012,
    2590947315873921485,
    1443031110135629158,
    7726419694724017893,
    772933552794012582,
    5448906529310011837,
    6632338414463930806,
    3847039018840058312,
    8265378659972700994,
    6163797010322633086,
    6969728053656791494,
    5956253119684311826,
    4636395439419093230,
    1359806940856786764,
    8699347003098897756,
    3799042485127264635,
    3290219653540828453,
    8519996453723328399,
    8206216686050112369,
    2165285721189832094,
    2817680779095892653,
    9139571285809587515,
    3913649871357130550,
    8707138651345200304,
    463108016820113542,
    4715274434274599084,
    5843929872280638345,
    6649016820453168018,
    3076626320123895538,
    356594457333858261,
    3815983352594277404,
    2512340383372501491,
    7467189659229575043,
    2283565563052273891,
]
UPPER_LOWER_BOUNDED_SEQUENCE = [
    136162455451213,
    216235431139227,
    196381922853526,
    91824374269877,
    104102812713490,
    200331376842768,
    54071253912698,
    219731065517829,
    8836711314987,
    64557087371062,
    32824255920428,
    35741811151685,
    85608574169966,
    241442624136858,
    273034416844347,
    37843405505324,
    258229319030648,
    244386081218064,
    204663863026139,
    204254921967596,
    171837887416807,
    86967610207389,
    42679670071644,
    113991906471741,
    47844608428544,
    178267855261615,
    30418887946183,
    31455100803808,
    7787192265992,
    172384615444020,
    247328482426385,
    75917833827699,
    273465482635168,
    138429774519635,
    73627679493105,
    5400040499671,
    115015711679363,
    239075786288320,
    236215609572922,
    44764918846189,
    19392366466456,
    214664523769511,
    114276962350399,
    128219444184830,
    20814041426742,
    25128399781433,
    190470633398785,
    109268690443054,
    139200529799330,
    81182905643746,
    53424663635346,
    263991170026402,
    174972335731803,
    231474356523024,
    221977110642230,
    152371566983537,
    197708040830710,
    55651508818525,
    94491148190674,
    230928487845345,
    272990384362848,
    205168316522100,
    114835994950908,
    128761962523644,
    211661687733390,
    87344717875886,
    239265471855755,
    213515137724411,
    6231793605967,
    259541210616528,
    90296284119585,
    110295863015468,
    107290805643263,
    107163877467039,
    246656863289141,
    105168348635553,
    56056877300273,
    226737146053996,
    197643616240816,
    39857808199647,
    261666746861755,
    214956565193432,
    141008019740089,
    212757036301581,
    77870195886731,
    36863357004409,
    240099532415543,
    146344012101761,
    179438507416655,
    20861790925725,
    262092690446671,
    177668434664038,
    178986416520290,
    195318720298788,
    242657484589767,
    241470097982931,
    4843884223768,
    31587317223049,
    115923058646656,
    95189363734870,
    141123990433569,
    176037409582797,
    110321992872044,
    217410074542379,
    156925321898262,
    87274739585082,
    11028236596419,
    190780286063478,
    278197846869077,
    210517344683334,
    80399702460563,
    174787943031240,
    226760440560308,
    221619595092571,
    150828263345248,
    205741254717439,
    102219922639897,
    146520154344451,
    178892232564701,
    253072570667843,
    172803954897842,
    268404702123838,
    12572317962733,
    187446827716584,
    145634942057607,
    152478951795678,
    147395314320406,
]


# This simple test ensures that the code size of this library doesn't grow unexpectedly if we
#  start taking subroutine inlining and opcode assembly opportunities.
def test_library_size(
    lib_pcg64_client: str,
    expected_library_size: int,
    request: pytest.FixtureRequest,
):
    client = request.getfixturevalue(lib_pcg64_client)
    assert len(client.app_client.approval.teal.split("\n")) < expected_library_size


def test_unbounded_maximal_cost(
    lib_pcg64_client: str,
    max_unbounded_opup_calls: int,
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg64_client)
    result = (
        client.compose()
        .bounded_rand_uint64(
            seed=RNG_SEED,
            lower_bound=0,
            upper_bound=0,
            length=EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
        )
        .simulate(SimulateOptions(extra_opcode_budget=320_000))
    )

    assert result.abi_results[0].return_value
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < 700 * max_unbounded_opup_calls
    )


def test_bounded_maximal_cost(
    lib_pcg64_client: str,
    max_bounded_opup_calls: int,
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg64_client)
    result = (
        client.compose()
        .bounded_rand_uint64(
            seed=RNG_SEED,
            lower_bound=1,
            upper_bound=2**64 - 1,
            length=EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
        )
        .simulate(SimulateOptions(extra_opcode_budget=320_000))
    )

    assert result.abi_results[0].return_value
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < 700 * max_bounded_opup_calls
    )


def test_unbounded_sequence(
    lib_pcg64_client: str,
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg64_client)
    result = (
        client.compose()
        .bounded_rand_uint64(
            seed=RNG_SEED,
            lower_bound=0,
            upper_bound=0,
            length=EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
        )
        .simulate(SimulateOptions(extra_opcode_budget=320_000))
    )

    assert result.abi_results[0].return_value == UNBOUNDED_SEQUENCE


def test_lower_bounded_sequence(
    lib_pcg64_client: str,
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg64_client)
    result = (
        client.compose()
        .bounded_rand_uint64(
            seed=RNG_SEED,
            lower_bound=2**63 - 1,
            upper_bound=0,
            length=EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
        )
        .simulate(SimulateOptions(extra_opcode_budget=320_000))
    )

    assert result.abi_results[0].return_value == LOWER_BOUNDED_SEQUENCE


def test_upper_bounded_sequence(
    lib_pcg64_client: str,
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg64_client)
    result = (
        client.compose()
        .bounded_rand_uint64(
            seed=RNG_SEED,
            lower_bound=0,
            upper_bound=2**63 + 1,
            length=EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
        )
        .simulate(SimulateOptions(extra_opcode_budget=320_000))
    )

    assert result.abi_results[0].return_value == UPPER_BOUNDED_SEQUENCE


def test_upper_lower_bounded_sequence(
    lib_pcg64_client: str,
    request: pytest.FixtureRequest,
) -> None:
    client = request.getfixturevalue(lib_pcg64_client)
    result = (
        client.compose()
        .bounded_rand_uint64(
            seed=RNG_SEED,
            lower_bound=2**16,
            upper_bound=2**48,
            length=EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
        )
        .simulate(SimulateOptions(extra_opcode_budget=320_000))
    )

    assert result.abi_results[0].return_value == UPPER_LOWER_BOUNDED_SEQUENCE
