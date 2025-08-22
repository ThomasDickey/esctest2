# The following CSI codes supported by xterm are not tested.
# Query ReGIS/Sixel attributes:  CSI ? Pi ; Pa ; P vS
# Initiate highlight mouse tracking: CSI Ps ; Ps ; Ps ; Ps ; Ps T
# Media Copy (MC): CSI Pm i
# Media Copy (MC, DEC-specific): CSI ? Pm i
# Character Attributes (SGR): CSI Pm m
# Disable modifiers: CSI > Ps n
# Set pointer mode: CSI > Ps p
# Load LEDs (DECLL): CSI Ps q
# Set cursor style (DECSCUSR): CIS Ps SP q
# Select character protection attribute (DECSCA): CSI Ps " q
#                                  [This is already tested by DECSED and DECSEL]
# Window manipulation: CSI Ps; Ps; Ps t
# Reverse Attributes in Rectangular Area (DECRARA): CSI Pt ; Pl ; Pb ; Pr ; Ps $ t
# Set warning bell volume (DECSWBV): CSI Ps SP t
# Set margin-bell volume (DECSMBV): CSI Ps SP u
# Enable Filter Rectangle (DECEFR): CSI Pt ; Pl ; Pb ; Pr ' w
# Request Terminal Parameters (DECREQTPARM): CSI Ps x
# Select Attribute Change Extent (DECSACE): CSI Ps * x
# Request Checksum of Rectangular Area (DECRQCRA): CSI Pi ; Pg ; Pt ; Pl ; Pb ; Pr * y
# Select Locator Events (DECSLE): CSI Pm ' {
# Request Locator Position (DECRQLP): CSI PS ' |
# ESC SP L  Set ANSI conformance level 1 (dpANS X3.134.1).
# ESC SP M  Set ANSI conformance level 2 (dpANS X3.134.1).
# ESC SP N  Set ANSI conformance level 3 (dpANS X3.134.1).
#   In xterm, all these do is fiddle with character sets, which are not testable.
# ESC # 3   DEC double-height line, top half (DECDHL).
# ESC # 4   DEC double-height line, bottom half (DECDHL).
# ESC # 5   DEC single-width line (DECSWL).
# ESC # 6   DEC double-width line (DECDWL).
#  Double-width affects display only and is generally not introspectable. Wrap
#  doesn't work so there's no way to tell where the cursor is visually.
# ESC % @   Select default character set.  That is ISO 8859-1 (ISO 2022).
# ESC % G   Select UTF-8 character set (ISO 2022).
# ESC ( C   Designate G0 Character Set (ISO 2022, VT100).
# ESC ) C   Designate G1 Character Set (ISO 2022, VT100).
# ESC * C   Designate G2 Character Set (ISO 2022, VT220).
# ESC + C   Designate G3 Character Set (ISO 2022, VT220).
# ESC - C   Designate G1 Character Set (VT300).
# ESC . C   Designate G2 Character Set (VT300).
# ESC / C   Designate G3 Character Set (VT300).
#  Character set stuff is not introspectable.
# Shift in (SI): ^O
# Shift out (SO): ^N
# Space (SP): 0x20
# Tab (TAB): 0x09 [tested in HTS]
# ESC =     Application Keypad (DECKPAM).
# ESC >     Normal Keypad (DECKPNM).
# ESC F     Cursor to lower left corner of screen.  This is enabled by the
#           hpLowerleftBugCompat resource. (Not worth testing as it's off by
#           default, and silly regardless)
# ESC l     Memory Lock (per HP terminals).  Locks memory above the cursor.
# ESC m     Memory Unlock (per HP terminals).
# ESC n     Invoke the G2 Character Set as GL (LS2).
# ESC o     Invoke the G3 Character Set as GL (LS3).
# ESC |     Invoke the G3 Character Set as GR (LS3R).
# ESC }     Invoke the G2 Character Set as GR (LS2R).
# ESC ~     Invoke the G1 Character Set as GR (LS1R).
# DCS + p Pt ST    Set Termcap/Terminfo Data
# DCS + q Pt ST    Request Termcap/Terminfo String
# The following OSC commands are tested in xterm_winops and don't have their own test:
#           Ps = 0  -> Change Icon Name and Window Title to Pt.
#           Ps = 1  -> Change Icon Name to Pt.
#           Ps = 2  -> Change Window Title to Pt.
# This test is too ill-defined and X-specific, and is not tested:
#           Ps = 3  -> Set X property on top-level window.  Pt should be
#         in the form "prop=value", or just "prop" to delete the prop-
#         erty
# No introspection for whether special color are enabled/disabled:
#           Ps = 6 ; c; f -> Enable/disable Special Color Number c.  The
#         second parameter tells xterm to enable the corresponding color
#         mode if nonzero, disable it if zero.
# Off by default, obvious security issues:
#           Ps = 4 6  -> Change Log File to Pt.  (This is normally dis-
#         abled by a compile-time option).
# No introspection for fonts:
#           Ps = 5 0  -> Set Font to Pt.
# No-op:
#           Ps = 5 1  -> reserved for Emacs shell.


from tests.apc import APCTests
from tests.bs import BSTests
from tests.cbt import CBTTests
from tests.cha import CHATests
from tests.change_color import ChangeColorTests
from tests.change_dynamic_color import ChangeDynamicColorTests
from tests.change_special_color import ChangeSpecialColorTests
from tests.cht import CHTTests
from tests.cnl import CNLTests
from tests.cpl import CPLTests
from tests.cr import CRTests
from tests.cub import CUBTests
from tests.cud import CUDTests
from tests.cuf import CUFTests
from tests.cup import CUPTests
from tests.cuu import CUUTests
from tests.da import DATests
from tests.da2 import DA2Tests
from tests.dch import DCHTests
from tests.dcs import DCSTests
from tests.decaln import DECALNTests
from tests.decbi import DECBITests
from tests.deccra import DECCRATests
from tests.decdc import DECDCTests
from tests.decdsr import DECDSRTests
from tests.decera import DECERATests
from tests.decfi import DECFITests
from tests.decfra import DECFRATests
from tests.decic import DECICTests
from tests.decid import DECIDTests
from tests.decrc import DECRCTests
from tests.decrqm import DECRQMTests
from tests.decrqss import DECRQSSTests
from tests.decscl import DECSCLTests
from tests.decsed import DECSEDTests
from tests.decsel import DECSELTests
from tests.decsera import DECSERATests
from tests.decset import DECSETTests
from tests.decset_tite_inhibit import DECSETTiteInhibitTests
from tests.decstbm import DECSTBMTests
from tests.decstr import DECSTRTests
from tests.dl import DLTests
from tests.ech import ECHTests
from tests.ed import EDTests
from tests.el import ELTests
from tests.ff import FFTests
from tests.hpa import HPATests
from tests.hpr import HPRTests
from tests.hts import HTSTests
from tests.hvp import HVPTests
from tests.ich import ICHTests
from tests.il import ILTests
from tests.ind import INDTests
from tests.lf import LFTests
from tests.manipulate_selection_data import ManipulateSelectionDataTests
from tests.nel import NELTests
from tests.pm import PMTests
from tests.rep import REPTests
from tests.reset_color import ResetColorTests
from tests.reset_special_color import ResetSpecialColorTests
from tests.ri import RITests
from tests.ris import RISTests
from tests.rm import RMTests
from tests.s8c1t import S8C1TTests
from tests.scorc import SCORCTests
from tests.sd import SDTests
from tests.sm import SMTests
from tests.sm_title import SMTitleTests
from tests.sos import SOSTests
from tests.su import SUTests
from tests.tbc import TBCTests
from tests.vpa import VPATests
from tests.vpr import VPRTests
from tests.vt import VTTests
from tests.xterm_save import XtermSaveTests
from tests.xterm_winops import XtermWinopsTests

tests = [
    APCTests,
    BSTests,
    CBTTests,
    CHATests,
    CHTTests,
    CNLTests,
    CPLTests,
    CRTests,
    CUBTests,
    CUDTests,
    CUFTests,
    CUPTests,
    CUUTests,
    ChangeColorTests,
    ChangeDynamicColorTests,
    ChangeSpecialColorTests,
    DA2Tests,
    DATests,
    DCHTests,
    DCSTests,
    DECALNTests,
    DECBITests,
    DECCRATests,
    DECDCTests,
    DECDSRTests,
    DECERATests,
    DECFITests,
    DECFRATests,
    DECICTests,
    DECIDTests,
    DECRCTests,
    DECRQMTests,
    DECRQSSTests,
    DECSCLTests,
    DECSEDTests,
    DECSELTests,
    DECSERATests,
    DECSETTests,
    DECSETTiteInhibitTests,
    DECSTBMTests,
    DECSTRTests,
    DLTests,
    ECHTests,
    EDTests,
    ELTests,
    FFTests,
    HPATests,
    HPRTests,
    HTSTests,
    HVPTests,
    ICHTests,
    ILTests,
    INDTests,
    LFTests,
    ManipulateSelectionDataTests,
    NELTests,
    PMTests,
    REPTests,
    RISTests,
    RITests,
    RMTests,
    ResetColorTests,
    ResetSpecialColorTests,
    S8C1TTests,
    SCORCTests,
    SDTests,
    SMTests,
    SMTitleTests,
    SOSTests,
    SUTests,
    TBCTests,
    VPATests,
    VPRTests,
    VTTests,
    XtermSaveTests,
    XtermWinopsTests,
    ]
