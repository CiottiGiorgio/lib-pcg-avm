from collections.abc import Callable
from typing import Any

import algokit_utils
import pytest
from algokit_utils import (
    AlgorandClient,
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
                metafunc.parametrize("max_bounded_opup_calls", [22])
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
        compilation_params={"updatable": True, "deletable": True},
    )

    return client


RNG_SEED = (
    b"\x00\x00\x00\x00\x00\x00\x00\x2a"
    + b"\x00\x00\x00\x00\x00\x00\x00\x36"
    + b"\x00\x00\x00\x00\x00\x00\x00\x2a"
    + b"\x00\x00\x00\x00\x00\x00\x00\x36"
)

EXPECTED_MAXIMAL_SEQUENCE_LENGTH = 63
# These sequences WERE NOT generated using the reference C implementation.
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
# LOWER_BOUNDED_SEQUENCE = [
#     14048270771836679755,
#     17703472758907470352,
#     14683759177899822200,
#     15415759776988739331,
#     18380099057036996404,
#     13081300888861161770,
#     17930197454918215320,
#     16498647315493842489,
#     12969499253219514230,
#     13935185923691857898,
#     15639681094942944411,
#     12348068430114775386,
#     17366557100957019963,
#     11808616488071270317,
#     10400531842137922270,
#     9590423191444729094,
#     15885850585402998287,
#     10648471831967459230,
#     16326748173002968047,
#     13385547914399115733,
#     9474562729586353025,
#     12991998097818381502,
#     15518016329788511638,
#     9326325065706464933,
#     9952135877641223735,
#     12168072236025225727,
#     13953416742781622432,
#     11557443723954205408,
#     9268461455634081168,
#     15955391567321942944,
#     9259575804053533785,
#     10280260571389530126,
#     10735653317285641972,
#     13947985169204384347,
#     16298621538807153616,
#     13832454963982154892,
#     15960151916226739337,
#     11199867386943230670,
#     10619032259719374845,
#     18352133659148402483,
#     15536679454229258655,
#     13010000157683434858,
#     16746269904140944558,
#     9466546606298826937,
#     16515196261264253654,
#     11655528589957365003,
#     16535043898236750473,
#     10998390100788357751,
#     11431501851043963445,
#     18406639491766368383,
#     12994876108566115227,
#     14971071675514378573,
#     12725116062892818210,
#     10903175877833247429,
#     12549003727653543190,
#     16586591871825567358,
#     13817138842919319892,
#     16318652894991200031,
#     10818038099394703466,
#     9483672323201859881,
#     18025105582636725441,
#     11990461835414819700,
#     16895250721016841299,
#     17864317628199680690,
#     18224881932436611673,
#     15102923566793133079,
#     9539333478657395713,
#     9445724195982350140,
#     12520863958422770155,
#     11829701322416188380,
#     15244572036978279514,
#     15204276443289332059,
#     17520215145058845268,
#     12818048997932234705,
#     10857162122855097677,
#     11057895448646740158,
#     12898076259823057623,
#     16764247759469818902,
#     13597544016353148519,
#     16590742698129821942,
#     14608127200177485471,
#     17036869519386771727,
#     13635697290629213735,
#     16795821605013781237,
#     13485880563821517916,
#     11837950670804688225,
#     13174788898569943146,
#     17826452549728959091,
#     12574775152811025531,
#     15372247455199486572,
#     18161195416760204539,
#     11084137688641389636,
#     11553716161079585695,
#     12173457528097282819,
#     11814319352728697292,
#     10666403146990404965,
#     16949791731578793700,
#     9996305589648788389,
#     14672278566164787644,
#     15855710451318706613,
#     13070411055694834119,
#     17488750696827476801,
#     15387169047177408893,
#     16193100090511567301,
#     15179625156539087633,
#     13859767476273869037,
#     10583178977711562571,
#     17922719039953673563,
#     13022414521982040442,
#     12513591690395604260,
#     17743368490578104206,
#     17429588722904888176,
#     11388657758044607901,
#     12041052815950668460,
#     18362943322664363322,
#     13137021908211906357,
#     17930510688199976111,
#     9686480053674889349,
#     13938646471129374891,
#     15067301909135414152,
#     15872388857307943825,
#     12299998356978671345,
#     9579966494188634068,
#     13039355389449053211,
#     11735712420227277298,
#     16690561696084350850,
#     11506937599907049698,
# ]
# UPPER_BOUNDED_SEQUENCE = [
#     4824898734981903948,
#     8480100722052694545,
#     5460387141045046393,
#     6192387740133963524,
#     9156727020182220597,
#     3857928852006385963,
#     8706825418063439513,
#     7275275278639066682,
#     3746127216364738423,
#     4711813886837082091,
#     6416309058088168604,
#     3124696393259999579,
#     8143185064102244156,
#     2585244451216494510,
#     1177159805283146463,
#     367051154589953287,
#     6662478548548222480,
#     1425099795112683423,
#     7103376136148192240,
#     4162175877544339926,
#     251190692731577218,
#     3768626060963605695,
#     6294644292933735831,
#     102953028851689126,
#     728763840786447928,
#     2944700199170449920,
#     4730044705926846625,
#     2334071687099429601,
#     45089418779305361,
#     6732019530467167137,
#     36203767198757978,
#     1056888534534754319,
#     1512281280430866165,
#     4724613132349608540,
#     7075249501952377809,
#     4609082927127379085,
#     6736779879371963530,
#     1976495350088454863,
#     1395660222864599038,
#     9128761622293626676,
#     6313307417374482848,
#     3786628120828659051,
#     7522897867286168751,
#     243174569444051130,
#     7291824224409477847,
#     2432156553102589196,
#     7311671861381974666,
#     1775018063933581944,
#     2208129814189187638,
#     9183267454911592576,
#     3771504071711339420,
#     5747699638659602766,
#     3501744026038042403,
#     1679803840978471622,
#     3325631690798767383,
#     7363219834970791551,
#     4593766806064544085,
#     7095280858136424224,
#     1594666062539927659,
#     260300286347084074,
#     8801733545781949634,
#     2767089798560043893,
#     7671878684162065492,
#     8640945591344904883,
#     9001509895581835866,
#     5879551529938357272,
#     315961441802619906,
#     222352159127574333,
#     3297491921567994348,
#     2606329285561412573,
#     6021200000123503707,
#     5980904406434556252,
#     8296843108204069461,
#     3594676961077458898,
#     1633790086000321870,
#     1834523411791964351,
#     3674704222968281816,
#     7540875722615043095,
#     4374171979498372712,
#     7367370661275046135,
#     5384755163322709664,
#     7813497482531995920,
#     4412325253774437928,
#     7572449568159005430,
#     4262508526966742109,
#     2614578633949912418,
#     3951416861715167339,
#     8603080512874183284,
#     3351403115956249724,
#     6148875418344710765,
#     8937823379905428732,
#     1860765651786613829,
#     2330344124224809888,
#     2950085491242507012,
#     2590947315873921485,
#     1443031110135629158,
#     7726419694724017893,
#     772933552794012582,
#     5448906529310011837,
#     6632338414463930806,
#     3847039018840058312,
#     8265378659972700994,
#     6163797010322633086,
#     6969728053656791494,
#     5956253119684311826,
#     4636395439419093230,
#     1359806940856786764,
#     8699347003098897756,
#     3799042485127264635,
#     3290219653540828453,
#     8519996453723328399,
#     8206216686050112369,
#     2165285721189832094,
#     2817680779095892653,
#     9139571285809587515,
#     3913649871357130550,
#     8707138651345200304,
#     463108016820113542,
#     4715274434274599084,
#     5843929872280638345,
#     6649016820453168018,
#     3076626320123895538,
#     356594457333858261,
#     3815983352594277404,
#     2512340383372501491,
#     7467189659229575043,
#     2283565563052273891,
# ]
# UPPER_LOWER_BOUNDED_SEQUENCE = [
#     136162455451213,
#     216235431139227,
#     196381922853526,
#     91824374269877,
#     104102812713490,
#     200331376842768,
#     54071253912698,
#     219731065517829,
#     8836711314987,
#     64557087371062,
#     32824255920428,
#     35741811151685,
#     85608574169966,
#     241442624136858,
#     273034416844347,
#     37843405505324,
#     258229319030648,
#     244386081218064,
#     204663863026139,
#     204254921967596,
#     171837887416807,
#     86967610207389,
#     42679670071644,
#     113991906471741,
#     47844608428544,
#     178267855261615,
#     30418887946183,
#     31455100803808,
#     7787192265992,
#     172384615444020,
#     247328482426385,
#     75917833827699,
#     273465482635168,
#     138429774519635,
#     73627679493105,
#     5400040499671,
#     115015711679363,
#     239075786288320,
#     236215609572922,
#     44764918846189,
#     19392366466456,
#     214664523769511,
#     114276962350399,
#     128219444184830,
#     20814041426742,
#     25128399781433,
#     190470633398785,
#     109268690443054,
#     139200529799330,
#     81182905643746,
#     53424663635346,
#     263991170026402,
#     174972335731803,
#     231474356523024,
#     221977110642230,
#     152371566983537,
#     197708040830710,
#     55651508818525,
#     94491148190674,
#     230928487845345,
#     272990384362848,
#     205168316522100,
#     114835994950908,
#     128761962523644,
#     211661687733390,
#     87344717875886,
#     239265471855755,
#     213515137724411,
#     6231793605967,
#     259541210616528,
#     90296284119585,
#     110295863015468,
#     107290805643263,
#     107163877467039,
#     246656863289141,
#     105168348635553,
#     56056877300273,
#     226737146053996,
#     197643616240816,
#     39857808199647,
#     261666746861755,
#     214956565193432,
#     141008019740089,
#     212757036301581,
#     77870195886731,
#     36863357004409,
#     240099532415543,
#     146344012101761,
#     179438507416655,
#     20861790925725,
#     262092690446671,
#     177668434664038,
#     178986416520290,
#     195318720298788,
#     242657484589767,
#     241470097982931,
#     4843884223768,
#     31587317223049,
#     115923058646656,
#     95189363734870,
#     141123990433569,
#     176037409582797,
#     110321992872044,
#     217410074542379,
#     156925321898262,
#     87274739585082,
#     11028236596419,
#     190780286063478,
#     278197846869077,
#     210517344683334,
#     80399702460563,
#     174787943031240,
#     226760440560308,
#     221619595092571,
#     150828263345248,
#     205741254717439,
#     102219922639897,
#     146520154344451,
#     178892232564701,
#     253072570667843,
#     172803954897842,
#     268404702123838,
#     12572317962733,
#     187446827716584,
#     145634942057607,
#     152478951795678,
#     147395314320406,
# ]


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


# def test_lower_bounded_sequence(
#     lib_pcg64_client: str,
#     request: pytest.FixtureRequest,
# ) -> None:
#     client = request.getfixturevalue(lib_pcg64_client)
#     result = (
#         client.compose()
#         .bounded_rand_uint128(
#             seed=RNG_SEED,
#             lower_bound=2**63 - 1,
#             upper_bound=0,
#             length=EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
#         )
#         .simulate(SimulateOptions(extra_opcode_budget=320_000))
#     )
#
#     assert result.returns[0].value == LOWER_BOUNDED_SEQUENCE
#
#
# def test_upper_bounded_sequence(
#     lib_pcg64_client: str,
#     request: pytest.FixtureRequest,
# ) -> None:
#     client = request.getfixturevalue(lib_pcg64_client)
#     result = (
#         client.compose()
#         .bounded_rand_uint128(
#             seed=RNG_SEED,
#             lower_bound=0,
#             upper_bound=2**63 + 1,
#             length=EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
#         )
#         .simulate(SimulateOptions(extra_opcode_budget=320_000))
#     )
#
#     assert result.returns[0].value == UPPER_BOUNDED_SEQUENCE
#
#
# def test_upper_lower_bounded_sequence(
#     lib_pcg64_client: str,
#     request: pytest.FixtureRequest,
# ) -> None:
#     client = request.getfixturevalue(lib_pcg64_client)
#     result = (
#         client.compose()
#         .bounded_rand_uint128(
#             seed=RNG_SEED,
#             lower_bound=2**16,
#             upper_bound=2**48,
#             length=EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
#         )
#         .simulate(SimulateOptions(extra_opcode_budget=320_000))
#     )
#
#     assert result.returns[0].value == UPPER_LOWER_BOUNDED_SEQUENCE
