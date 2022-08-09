import ROOT as R
import logging
import yaml
from itertools import cycle
logger = logging.getLogger(__name__)
import os

#loads the plot names from the text file into a list
plot_names = list()
data_file_names = open("data_plot_names.txt", "r")
plot_names = [line.strip() for line in data_file_names.readlines() if line]
data_file_names.close()

COL_STORE = []
labels_path = 'Dumbledraw/Dumbledraw/labels.yaml'


def CreateTransparentColor(color, alpha):
    adapt = R.gROOT.GetColor(color)
    new_idx = R.gROOT.GetListOfColors().GetLast() + 1
    trans = R.TColor(new_idx, adapt.GetRed(), adapt.GetGreen(),
                     adapt.GetBlue(), '', alpha)
    COL_STORE.append(trans)
    trans.SetName('userColor%i' % new_idx)
    return new_idx


legend_label_dict = yaml.load(open(labels_path))['legend_label']
x_label_dict = yaml.load(open(labels_path))['x_label']

mass_dict= yaml.load(open("shapes/mass_dict_nmssm.yaml"), Loader=yaml.Loader)["plots"]


color_dict = {
    "data": R.TColor.GetColor(0,0,0),
    "ggH": R.TColor.GetColor("#fed766"),
    "qqH": R.TColor.GetColor("#2ab7ca"),
    "ggH125": R.TColor.GetColor("#BF2229"),
    "qqH125": R.TColor.GetColor("#00A88F"),
    "HTT": R.TColor.GetColor("#00A88F"),
    "VH": R.TColor.GetColor("#001EFF"),
    "WH": R.TColor.GetColor("#001EFF"),
    "ZH": R.TColor.GetColor("#001EFF"),
    "ttH": R.TColor.GetColor("#FF00FF"),
    "HWW": R.TColor.GetColor("#FF8C00"),
    "ggH_hww": R.TColor.GetColor("#FF8C00"),
    "qqH_hww": R.TColor.GetColor("#FF8C00"),
    "dummy": R.TColor.GetColor(254, 74, 73),
    "inclusive": R.TColor.GetColor(254, 74, 73),
    "ZTT": R.TColor.GetColor(248, 206, 104),
    "EMB": R.TColor.GetColor(248, 206, 104),
    "ZLL": R.TColor.GetColor(100, 192, 232),
    "ZL": R.TColor.GetColor(100, 192, 232),
    "ZJ": R.TColor.GetColor("#64DE6A"),
    "TT": R.TColor.GetColor(155, 152, 204),
    "TTT": R.TColor.GetColor(155, 152, 204),
    "TTL": R.TColor.GetColor(155, 152, 204),
    "TTJ": R.TColor.GetColor(215, 130, 204),
    "W": R.TColor.GetColor(222, 90, 106),
    "WT": R.TColor.GetColor(222, 90, 106),
    "WL": R.TColor.GetColor(222, 150, 80),
    "VV": R.TColor.GetColor("#6F2D35"),
    "VVT": R.TColor.GetColor("#6F2D35"),
    "VVJ": R.TColor.GetColor("#c38a91"),
    "VVL" : R.TColor.GetColor("#6F2D35"),
    "ST": R.TColor.GetColor("#d0f0c1"),
    "STT": R.TColor.GetColor("#d0f0c1"),
    "STL" : R.TColor.GetColor("#d0f0c1"),
    "QCD": R.TColor.GetColor(250, 202, 255),
    "QCDEMB": R.TColor.GetColor(250, 202, 255),
    "EWK": R.TColor.GetColor("#E1F5A9"),
    "EWKT": R.TColor.GetColor("#E1F5A9"),
    "EWKL": R.TColor.GetColor("#E1F5A9"),
    "EWKJ": R.TColor.GetColor("#E1F5A9"),
    "EWKZ": R.TColor.GetColor("#E1F5A9"),
    "jetFakes": R.TColor.GetColor(192, 232, 100),
    "jetFakesW": R.TColor.GetColor(222, 90, 106),
    "jetFakesQCD": R.TColor.GetColor(250, 202, 255),
    "jetFakesTT": R.TColor.GetColor(155, 152, 204),
    "jetFakesEMB": R.TColor.GetColor(192, 232, 100),
    "jetFakesCMB": R.TColor.GetColor(250, 202, 255),
    "TotalBkg": R.TColor.GetColor(211,211,211),
    "REST": R.TColor.GetColor("#B0C4DE"),
    "unc": CreateTransparentColor(12, 0.4)

}

#creates different colors for the different run numbers
if plot_names[0] != "data":
    counter =0.0
    for plot in plot_names:
        counter+=1.0
        if counter%2:
            r=int(255.0-255.0*(counter/len(plot_names)))
            b = int(255.0*(counter/len(plot_names)))
            g = 0
        else:
            r=int(255.0-255.0*(counter/len(plot_names)))
            g = int(255.0*(counter/len(plot_names)))
            b = 20
        color_dict[plot] = R.TColor.GetColor(r, g, b)


i=0
colors=["#8B008B", "#008a8a", "#8a0022", "#22008a","#8a8a00"]
sig_colors=cycle(colors)
for heavy_mass in mass_dict["heavy_mass"]:
    light_masses = mass_dict["light_mass_coarse"] if heavy_mass > 1001 else mass_dict["light_mass_fine"]
    for color in sig_colors:
        if i<len(light_masses):
            if light_masses[i]+125<heavy_mass:
                color_dict["NMSSM_{heavy_mass}_125_{light_mass}".format(heavy_mass=heavy_mass,light_mass=light_masses[i])] = R.TColor.GetColor(color)
                i+=1
        else:
            break

def SetStyle(name, **kwargs):
    styles = {"none": none, "TDR": SetTDRStyle, "ModTDR": ModTDRStyle}
    if not name in styles.keys():
        logger.fatal("%s style not available!" % name)
    logger.info("Set plotting style to %s" % name)
    styles[name](**kwargs)


def none():
    pass


def SetTDRStyle():
    """Sets the PubComm recommended style
    Just a copy of <http://ghm.web.cern.ch/ghm/plots/MacroExample/tdrstyle.C>
    @sa ModTDRStyle() to use this style with some additional customisation.
    """
    # For the canvas:
    R.gStyle.SetCanvasBorderMode(0)
    R.gStyle.SetCanvasColor(R.kWhite)
    R.gStyle.SetCanvasDefH(600)  # Height of canvas
    R.gStyle.SetCanvasDefW(600)  # Width of canvas
    R.gStyle.SetCanvasDefX(0)  # POsition on screen
    R.gStyle.SetCanvasDefY(0)

    # For the Pad:
    R.gStyle.SetPadBorderMode(0)
    # R.gStyle.SetPadBorderSize(Width_t size = 1)
    R.gStyle.SetPadColor(R.kWhite)
    R.gStyle.SetPadGridX(False)
    R.gStyle.SetPadGridY(False)
    R.gStyle.SetGridColor(0)
    R.gStyle.SetGridStyle(3)
    R.gStyle.SetGridWidth(1)

    # For the frame:
    R.gStyle.SetFrameBorderMode(0)
    R.gStyle.SetFrameBorderSize(1)
    R.gStyle.SetFrameFillColor(0)
    R.gStyle.SetFrameFillStyle(0)
    R.gStyle.SetFrameLineColor(1)
    R.gStyle.SetFrameLineStyle(1)
    R.gStyle.SetFrameLineWidth(1)

    # For the histo:
    # R.gStyle.SetHistFillColor(1)
    # R.gStyle.SetHistFillStyle(0)
    R.gStyle.SetHistLineColor(1)
    R.gStyle.SetHistLineStyle(0)
    R.gStyle.SetHistLineWidth(1)
    # R.gStyle.SetLegoInnerR(Float_t rad = 0.5)
    # R.gStyle.SetNumberContours(Int_t number = 20)

    R.gStyle.SetEndErrorSize(2)
    # R.gStyle.SetErrorMarker(20)
    # R.gStyle.SetErrorX(0.)

    R.gStyle.SetMarkerStyle(20)

    # For the fit/function:
    R.gStyle.SetOptFit(1)
    R.gStyle.SetFitFormat('5.4g')
    R.gStyle.SetFuncColor(2)
    R.gStyle.SetFuncStyle(1)
    R.gStyle.SetFuncWidth(1)

    # For the date:
    R.gStyle.SetOptDate(0)
    # R.gStyle.SetDateX(Float_t x = 0.01)
    # R.gStyle.SetDateY(Float_t y = 0.01)

    # For the statistics box:
    R.gStyle.SetOptFile(0)
    R.gStyle.SetOptStat(0)
    # To display the mean and RMS:   SetOptStat('mr')
    R.gStyle.SetStatColor(R.kWhite)
    R.gStyle.SetStatFont(42)
    R.gStyle.SetStatFontSize(0.025)
    R.gStyle.SetStatTextColor(1)
    R.gStyle.SetStatFormat('6.4g')
    R.gStyle.SetStatBorderSize(1)
    R.gStyle.SetStatH(0.1)
    R.gStyle.SetStatW(0.15)
    # R.gStyle.SetStatStyle(Style_t style = 1001)
    # R.gStyle.SetStatX(Float_t x = 0)
    # R.gStyle.SetStatY(Float_t y = 0)

    # Margins:
    R.gStyle.SetPadTopMargin(0.05)
    R.gStyle.SetPadBottomMargin(0.13)
    R.gStyle.SetPadLeftMargin(0.16)
    R.gStyle.SetPadRightMargin(0.02)

    # For the Global title:
    R.gStyle.SetOptTitle(0)
    R.gStyle.SetTitleFont(42)
    R.gStyle.SetTitleColor(1)
    R.gStyle.SetTitleTextColor(1)
    R.gStyle.SetTitleFillColor(10)
    R.gStyle.SetTitleFontSize(0.05)
    # R.gStyle.SetTitleH(0); # Set the height of the title box
    # R.gStyle.SetTitleW(0); # Set the width of the title box
    # R.gStyle.SetTitleX(0); # Set the position of the title box
    # R.gStyle.SetTitleY(0.985); # Set the position of the title box
    # R.gStyle.SetTitleStyle(Style_t style = 1001)
    # R.gStyle.SetTitleBorderSize(2)

    # For the axis titles:
    R.gStyle.SetTitleColor(1, 'XYZ')
    R.gStyle.SetTitleFont(42, 'XYZ')
    R.gStyle.SetTitleSize(0.06, 'XYZ')
    # Another way to set the size?
    # R.gStyle.SetTitleXSize(Float_t size = 0.02)
    # R.gStyle.SetTitleYSize(Float_t size = 0.02)
    R.gStyle.SetTitleXOffset(0.9)
    R.gStyle.SetTitleYOffset(1.25)
    # R.gStyle.SetTitleOffset(1.1, 'Y'); # Another way to set the Offset

    # For the axis labels:

    R.gStyle.SetLabelColor(1, 'XYZ')
    R.gStyle.SetLabelFont(42, 'XYZ')
    R.gStyle.SetLabelOffset(0.007, 'XYZ')
    R.gStyle.SetLabelSize(0.05, 'XYZ')

    # For the axis:

    R.gStyle.SetAxisColor(1, 'XYZ')
    R.gStyle.SetStripDecimals(True)
    R.gStyle.SetTickLength(0.03, 'XYZ')
    R.gStyle.SetNdivisions(510, 'XYZ')
    R.gStyle.SetPadTickX(1)
    R.gStyle.SetPadTickY(1)

    # Change for log plots:
    R.gStyle.SetOptLogx(0)
    R.gStyle.SetOptLogy(0)
    R.gStyle.SetOptLogz(0)

    # Postscript options:
    R.gStyle.SetPaperSize(20., 20.)
    # R.gStyle.SetLineScalePS(Float_t scale = 3)
    # R.gStyle.SetLineStyleString(Int_t i, const char* text)
    # R.gStyle.SetHeaderPS(const char* header)
    # R.gStyle.SetTitlePS(const char* pstitle)

    # R.gStyle.SetBarOffset(Float_t baroff = 0.5)
    # R.gStyle.SetBarWidth(Float_t barwidth = 0.5)
    # R.gStyle.SetPaintTextFormat(const char* format = 'g')
    # R.gStyle.SetPalette(Int_t ncolors = 0, Int_t* colors = 0)
    # R.gStyle.SetTimeOffset(Double_t toffset)
    # R.gStyle.SetHistMinimumZero(kTRUE)

    R.gStyle.SetHatchesLineWidth(5)
    R.gStyle.SetHatchesSpacing(0.05)


def ModTDRStyle(width=600, height=600, t=0.06, b=0.12, l=0.16, r=0.04):
    """Modified version of the tdrStyle
    Args:
        width (int): Canvas width in pixels
        height (int): Canvas height in pixels
        t (float): Pad top margin [0-1]
        b (float): Pad bottom margin [0-1]
        l (float): Pad left margin [0-1]
        r (float): Pad right margin [0-1]
    """
    SetTDRStyle()

    # Set the default canvas width and height in pixels
    R.gStyle.SetCanvasDefW(width)
    R.gStyle.SetCanvasDefH(height)

    # Set the default margins. These are given as fractions of the pad height
    # for `Top` and `Bottom` and the pad width for `Left` and `Right`. But we
    # want to specify all of these as fractions of the shortest length.
    def_w = float(R.gStyle.GetCanvasDefW())
    def_h = float(R.gStyle.GetCanvasDefH())

    scale_h = (def_w / def_h) if (def_h > def_w) else 1.
    scale_w = (def_h / def_w) if (def_w > def_h) else 1.

    def_min = def_h if (def_h < def_w) else def_w

    R.gStyle.SetPadTopMargin(t * scale_h)
    # default 0.05
    R.gStyle.SetPadBottomMargin(b * scale_h)
    # default 0.13
    R.gStyle.SetPadLeftMargin(l * scale_w)
    # default 0.16
    R.gStyle.SetPadRightMargin(r * scale_w)
    # default 0.02
    # But note the new CMS style sets these:
    # 0.08, 0.12, 0.12, 0.04

    # Set number of axis tick divisions
    R.gStyle.SetNdivisions(506, 'XYZ')  # default 510

    # Some marker properties not set in the default tdr style
    #R.gStyle.SetMarkerColor(R.kBlack)
    R.gStyle.SetMarkerSize(1.0)

    R.gStyle.SetLabelOffset(0.007, 'YZ')
    # This is an adhoc adjustment to scale the x-axis label
    # offset when we stretch plot vertically
    # Will also need to increase if first x-axis label has more than one digit
    R.gStyle.SetLabelOffset(0.005 * (3. - 2. / scale_h), 'X')

    # In this next part we do a slightly involved calculation to set the axis
    # title offsets, depending on the values of the TPad dimensions and
    # margins. This is to try and ensure that regardless of how these pad
    # values are set, the axis titles will be located towards the edges of the
    # canvas and not get pushed off the edge - which can often happen if a
    # fixed value is used.
    title_size = 0.05
    title_px = title_size * def_min
    label_size = 0.04
    R.gStyle.SetTitleSize(title_size, 'XYZ')
    R.gStyle.SetLabelSize(label_size, 'XYZ')

    R.gStyle.SetTitleXOffset(
        0.5 * scale_h * (1.2 *
                         (def_h * b * scale_h - 0.6 * title_px)) / title_px)
    R.gStyle.SetTitleYOffset(
        0.5 * scale_w * (1.2 *
                         (def_w * l * scale_w - 0.6 * title_px)) / title_px)

    # Only draw ticks where we have an axis
    R.gStyle.SetPadTickX(0)
    R.gStyle.SetPadTickY(0)
    R.gStyle.SetTickLength(0.02, 'XYZ')

    R.gStyle.SetLegendBorderSize(0)
    R.gStyle.SetLegendFont(42)
    R.gStyle.SetLegendFillColor(0)
    #R.gStyle.SetFillColor(0)

    R.gROOT.ForceStyle()

    R.TGaxis.SetExponentOffset(-0.07, 0.0, "y");

def DrawText(pad, text, scale_text_size, pos, angle, custom_pos = None):
    pad.cd()
    left_border = pad.GetLeftMargin()
    right_border = 1.0 - pad.GetRightMargin()
    top_border = 1.0 - pad.GetTopMargin()
    bottom_border = pad.GetBottomMargin()
    
    x_pos = 0.0
    y_pos = 0.0
    alignment = 22
    
    if custom_pos != None:
        if not (isinstance(custom_pos, list) and len(custom_pos) == 2):
            logger.fatal("Custom text position must be list with two entries, i.e. relative x and y coordinate in the pad")
            raise Exception
        else:
            x_pos = left_border + custom_pos[0] * (right_border - left_border)
            y_pos = bottom_border + custom_pos[0] * (top_border - bottom_border)
    else:
        if pos >= 1 and pos <= 9:
            pos = pos - 1
            x_pos = left_border + (0.07 + (pos % 3) * 0.43) * (right_border - left_border)
            y_pos = top_border + (0.07 + (pos / 3) * 0.43) * (bottom_border - top_border)
            alignment = 10 * ((pos % 3) + 1) + 3 - (pos / 3)
            if angle == 90:
                alignment = 10 * (alignment % 10) + 4 - alignment / 10
            elif angle == 270 or angle == -90:
                alignment = 40 - 10 * (alignment % 10) + alignment / 10
        else:
            logger.fatal("DrawText: pos must be in range [1 ... 9]")
            raise Exception

    latex = R.TLatex()
    latex.SetNDC()
    latex.SetTextAlign(alignment)
    latex.SetTextAngle(angle)
    latex.SetTextFont(42)
    latex.SetTextColor(R.kBlack)
    latex.SetTextSize(0.04 * scale_text_size)
    latex.DrawLatex(x_pos, y_pos, text)

def DrawCMSLogo(pad,
                cmsText,
                extraText,
                iPosX,
                relPosX,
                relPosY,
                relExtraDY,
                extraText2='',
                extraText3='',
                cmsTextSize=0.8):
    """Blah
    
    Args:
        pad (TYPE): Description
        cmsText (TYPE): Description
        extraText (TYPE): Description
        iPosX (TYPE): Description
        relPosX (TYPE): Description
        relPosY (TYPE): Description
        relExtraDY (TYPE): Description
        extraText2 (str): Description
        cmsTextSize (float): Description
    
    Returns:
        TYPE: Description
    """
    pad.cd()
    cmsTextFont = 62  # default is helvetic-bold

    writeExtraText = len(extraText) > 0
    writeExtraText2 = len(extraText2) > 0
    writeExtraText3 = len(extraText3) > 0
    extraTextFont = 52
    extraTextFont2and3 = 42


    # text sizes and text offsets with respect to the top frame
    # in unit of the top margin size
    lumiTextOffset = 0.2
    # cmsTextSize = 0.8
    # float cmsTextOffset    = 0.1;  // only used in outOfFrame version

    # ratio of 'CMS' and extra text size
    extraOverCmsTextSize = 0.76
    outOfFrame = False
    if iPosX / 10 == 0:
        outOfFrame = True

    alignY_ = 3
    alignX_ = 2
    if (iPosX / 10 == 0):
        alignX_ = 1
    if (iPosX == 0):
        alignX_ = 1
    if (iPosX == 0):
        alignY_ = 1
    if (iPosX / 10 == 1):
        alignX_ = 1
    if (iPosX / 10 == 2):
        alignX_ = 2
    if (iPosX / 10 == 3):
        alignX_ = 3
    # if (iPosX == 0): relPosX = 0.14
    align_ = 10 * alignX_ + alignY_

    l = pad.GetLeftMargin()
    t = pad.GetTopMargin()
    r = pad.GetRightMargin()
    b = pad.GetBottomMargin()

    latex = R.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(R.kBlack)

    extraTextSize = extraOverCmsTextSize * cmsTextSize
    pad_ratio = (float(pad.GetWh()) * pad.GetAbsHNDC()) / \
        (float(pad.GetWw()) * pad.GetAbsWNDC())
    if (pad_ratio < 1.):
        pad_ratio = 1.

    if outOfFrame:
        latex.SetTextFont(cmsTextFont)
        latex.SetTextAlign(11)
        latex.SetTextSize(cmsTextSize * t * pad_ratio)
        latex.DrawLatex(l, 1 - t + lumiTextOffset * t, cmsText)

    posX_ = 0
    if iPosX % 10 <= 1:
        posX_ = l + relPosX * (1 - l - r)
    elif (iPosX % 10 == 2):
        posX_ = l + 0.5 * (1 - l - r)
    elif (iPosX % 10 == 3):
        posX_ = 1 - r - relPosX * (1 - l - r)

    posY_ = 1 - t - relPosY * (1 - t - b)
    if not outOfFrame:
        latex.SetTextFont(cmsTextFont)
        latex.SetTextSize(cmsTextSize * t * pad_ratio)
        latex.SetTextAlign(align_)
        latex.DrawLatex(posX_, posY_, cmsText)
        if writeExtraText:
            latex.SetTextFont(extraTextFont)
            latex.SetTextAlign(align_)
            latex.SetTextSize(extraTextSize * t * pad_ratio)
            latex.DrawLatex(posX_, posY_ - relExtraDY * cmsTextSize * t,
                            extraText)
            if writeExtraText2:
                latex.SetTextFont(extraTextFont2and3)
                latex.DrawLatex(posX_,
                                posY_ - 1.8 * relExtraDY * cmsTextSize * t,
                                extraText2)
            if writeExtraText3:
                latex.SetTextFont(extraTextFont2and3)
                latex.DrawLatex(posX_,
                                posY_ - 2.6 * relExtraDY * cmsTextSize * t,
                                extraText3)
    elif writeExtraText:
        if iPosX == 0:
            posX_ = l + relPosX * (1 - l - r)
            posY_ = 1 - t + lumiTextOffset * t
        latex.SetTextFont(extraTextFont)
        latex.SetTextSize(extraTextSize * t * pad_ratio)
        latex.SetTextAlign(align_)
        latex.DrawLatex(posX_, posY_, extraText)


def DrawTitle(pad, text, align, textSize=0.6):
    pad_backup = R.gPad
    pad.cd()
    t = pad.GetTopMargin()
    l = pad.GetLeftMargin()
    r = pad.GetRightMargin()

    pad_ratio = (float(pad.GetWh()) * pad.GetAbsHNDC()) / \
        (float(pad.GetWw()) * pad.GetAbsWNDC())
    if pad_ratio < 1.:
        pad_ratio = 1.

    textOffset = 0.2

    latex = R.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(R.kBlack)
    latex.SetTextFont(42)
    latex.SetTextSize(textSize * t * pad_ratio)

    y_off = 1 - t + textOffset * t + 0.0055
    if align == 1:
        latex.SetTextAlign(11)
    if align == 1:
        latex.DrawLatex(l, y_off, text)
    if align == 2:
        latex.SetTextAlign(21)
    if align == 2:
        latex.DrawLatex(l + (1 - l - r) * 0.5, y_off, text)
    if align == 3:
        latex.SetTextAlign(31)
    if align == 3:
        latex.DrawLatex(1 - r, y_off, text)
    pad_backup.cd()
