# The following CSI codes supported by xcode are not tested.
# Query ReGIS/Sixel attributes:  CSI ? Pi ; Pa ; P vS
# Initiate highlight mouse tracking: CSI Ps ; Ps ; Ps ; Ps ; Ps T
# Media Copy (MC): CSI Pm i
# Media Copy (MC, DEC-specific): CSI ? Pm i
# Character Attributes (SGR): CSI Pm m
# Disable modifiers: CSI > Ps n
# Set pointer mode: CSI > Ps p
# Load LEDs (DECLL): CSI Ps q
# Set cursor style (DECSCUSR): CIS Ps SP q
# Select character protection attribute (DECSCA): CSI Ps " q   [This is already tested by DECSED and DECSEL]
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


import tests.ansirc
import tests.apc
import tests.bs
import tests.cbt
import tests.cha
import tests.change_color
import tests.change_special_color
import tests.change_dynamic_color
import tests.cht
import tests.cnl
import tests.cpl
import tests.cr
import tests.cub
import tests.cud
import tests.cuf
import tests.cup
import tests.cuu
import tests.da
import tests.da2
import tests.dch
import tests.dcs
import tests.decaln
import tests.decbi
import tests.deccra
import tests.decdc
import tests.decdsr
import tests.decera
import tests.decfra
import tests.decfi
import tests.decic
import tests.decid
import tests.decrc
import tests.decrqm
import tests.decrqss
import tests.decscl
import tests.decsed
import tests.decsel
import tests.decsera
import tests.decset
import tests.decset_tite_inhibit
import tests.decstbm
import tests.decstr
import tests.dl
import tests.ech
import tests.ed
import tests.el
import tests.ff
import tests.hpa
import tests.hpr
import tests.hts
import tests.hvp
import tests.ich
import tests.il
import tests.ind
import tests.lf
import tests.manipulate_selection_data
import tests.nel
import tests.pm
import tests.rep
import tests.reset_color
import tests.reset_special_color
import tests.ri
import tests.ris
import tests.rm
import tests.s8c1t
import tests.sd
import tests.sm
import tests.sm_title
import tests.sos
import tests.su
import tests.tbc
import tests.vpa
import tests.vpr
import tests.vt
import tests.xterm_save
import tests.xterm_winops

tests = [
    ansirc.ANSIRCTests,
    apc.APCTests,
    bs.BSTests,
    cbt.CBTTests,
    cha.CHATests,
    change_color.ChangeColorTests,
    change_special_color.ChangeSpecialColorTests,
    change_dynamic_color.ChangeDynamicColorTests,
    cht.CHTTests,
    cnl.CNLTests,
    cpl.CPLTests,
    cr.CRTests,
    cub.CUBTests,
    cud.CUDTests,
    cuf.CUFTests,
    cup.CUPTests,
    cuu.CUUTests,
    da.DATests,
    da2.DA2Tests,
    dch.DCHTests,
    dcs.DCSTests,
    decaln.DECALNTests,
    decbi.DECBITests,
    deccra.DECCRATests,
    decdc.DECDCTests,
    decdsr.DECDSRTests,
    decera.DECERATests,
    decfra.DECFRATests,
    decfi.DECFITests,
    decic.DECICTests,
    decid.DECIDTests,
    decrc.DECRCTests,
    decrqm.DECRQMTests,
    decrqss.DECRQSSTests,
    decscl.DECSCLTests,
    decsed.DECSEDTests,
    decsel.DECSELTests,
    decsera.DECSERATests,
    decset.DECSETTests,
    decset_tite_inhibit.DECSETTiteInhibitTests,
    decstbm.DECSTBMTests,
    decstr.DECSTRTests,
    dl.DLTests,
    ech.ECHTests,
    ed.EDTests,
    el.ELTests,
    ff.FFTests,
    hpa.HPATests,
    hpr.HPRTests,
    hts.HTSTests,
    hvp.HVPTests,
    ich.ICHTests,
    il.ILTests,
    ind.INDTests,
    lf.LFTests,
    manipulate_selection_data.ManipulateSelectionDataTests,
    nel.NELTests,
    pm.PMTests,
    rep.REPTests,
    reset_color.ResetColorTests,
    reset_special_color.ResetSpecialColorTests,
    ri.RITests,
    ris.RISTests,
    rm.RMTests,
    s8c1t.S8C1TTests,
    sd.SDTests,
    sm.SMTests,
    sm_title.SMTitleTests,
    sos.SOSTests,
    su.SUTests,
    tbc.TBCTests,
    vpa.VPATests,
    vpr.VPRTests,
    vt.VTTests,
    xterm_save.XtermSaveTests,
    xterm_winops.XtermWinopsTests,
    ]
