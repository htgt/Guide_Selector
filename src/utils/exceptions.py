class NoTargetRegionDataError(Exception):
    pass


class GetDataFromWGEError(Exception):
    pass


class ParseStringToTargetRegionError(Exception):
    pass


class GuideDeterminerError(Exception):
    pass


class MutatorError(Exception):
    pass


class PamNotFoundError(Exception):
    pass


class GuidesNotFoundError(Exception):
    pass


class NoGuidesRemainingError(Exception):
    pass


# copied from targeton-designer - need to use shared repo
class FileFormatError(Exception):
    pass


class FilterNotFoundException(Exception):
    def __init__(self, filter_name: str):
        super().__init__(f"The filter '{filter_name}' could not be found")
