from fastapi import FastAPI
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from schema import ModelInput, ModelOutput

from model import SentenceSimilarityBert

app = FastAPI(
    title='Flora backend',
    description='Flora backend that utilizes trained BERT to recommend items.',
    version='0.0.1',
    redoc_url=None,
    openapi_tags=[{
        'name': 'Flora backend',
        'description': 'Flora backend that utilizes trained BERT to recommend items.',
        'externalDocs': {
            'description': 'Gitlab',
            'url': 'https://gitlab.data-artist.com/2022_graduates/flora'
        }
    }]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.post('/predict', tags=['Backend'], status_code=200, response_model=ModelOutput)
def product_recommend(model_input: ModelInput):
    text = ''
    text += ' '.join(model_input.effects)
    text += ' '.join(model_input.skin_types)
    text += ' '.join(model_input.aroma_types)

    bert = SentenceSimilarityBert()
    bert.load_embeddings('./models/embeddings.pkl')
    
    bert_results = bert.get_product_idc(text)
    idc = list(bert_results.keys())
    percentages = list(bert_results.values())

    return { 'products_idx': idc, 'products_percentages': percentages }

    
@app.get("/", include_in_schema=False)
def main():
    return RedirectResponse(url="/docs/")
