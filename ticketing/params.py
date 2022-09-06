from drf_yasg import openapi

date = openapi.Parameter('date',
                              openapi.IN_QUERY, description="date param", type=openapi.TYPE_STRING)

customer = openapi.Parameter('customer',
                              openapi.IN_QUERY, description="customer param", type=openapi.TYPE_STRING)

type = openapi.Parameter('type',
                              openapi.IN_QUERY, description="type param", type=openapi.TYPE_STRING)

question =openapi.Parameter('question',
                              openapi.IN_QUERY, description="question param", type=openapi.TYPE_STRING)