# PHASE-2 MULTIMODAL FUSION MODULE

def fuse_inputs(ocr_text, voice_text=None):
    '''
    Fusion logic:
    Voice input overrides OCR if present
    '''
    if voice_text and len(voice_text.strip()) > 0:
        return voice_text
    return ocr_text
