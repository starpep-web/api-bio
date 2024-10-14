from fastapi import Request, Response
from pkg.handlers import router
from pkg.handlers.post_search_multi_query.service import create_multi_query_task
from pkg.shared.entity.search.multi_query.model import MultiAlignmentOptions
from pkg.shared.error.codes import ErrorCode
from pkg.shared.helpers.bio.fasta import parse_fasta_string, is_multi_fasta_valid
from pkg.shared.helpers.http.error import BadRequestException
from pkg.shared.helpers.http.response import ResponseBuilder
from pkg.shared.helpers.http.status import HttpStatus
from pkg.shared.helpers.http.headers import CONTENT_TYPE_FASTA


@router.post('/search/multi-query')
async def post(req: Request, res: Response):
    content_type = req.headers.get('Content-Type')
    if content_type != CONTENT_TYPE_FASTA:
        raise BadRequestException(f'Invalid request body type provided, must be {CONTENT_TYPE_FASTA}', ErrorCode.INVALID_BODY_PROVIDED)

    fasta_query_bytes = await req.body()
    fasta_query = fasta_query_bytes.decode('utf-8')
    parsed_fasta = parse_fasta_string(fasta_query)
    if not is_multi_fasta_valid(parsed_fasta):
        raise BadRequestException('Request body is not valid FASTA.', ErrorCode.INVALID_BODY_PROVIDED)

    try:
        options = MultiAlignmentOptions.create_from_params(dict(req.query_params))
    except ValueError as e:
        raise BadRequestException(str(e), ErrorCode.INVALID_QUERY_PROVIDED)

    task = create_multi_query_task(parsed_fasta, options)
    response = ResponseBuilder().with_status_code(HttpStatus.CREATED).with_data(task.get_init_status())

    res.status_code = response.code
    return response.build()
