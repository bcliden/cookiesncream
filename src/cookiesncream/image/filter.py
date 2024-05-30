from cookiesncream.lut import get_lut
from PIL.Image import Image
from pillow_lut import amplify_lut


def bw_filter(image: Image, intensity: float) -> Image:
    """
    The image filtering for the "Black and White" look
    """
    lut = get_lut("SoftBlackAndWhite")
    if lut is None:
        raise SystemError("LUT 'SoftBlackAndWhite' could not be located")
    amplified = amplify_lut(lut, intensity)
    image = image.filter(amplified)
    return image
