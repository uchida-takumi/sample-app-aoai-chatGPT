 #!/bin/sh
echo 'ここは prepdocs.sh です'
. ./scripts/loadenv.sh

echo 'Running "prepdocs.py"'
./.venv/bin/python ./scripts/prepdocs.py --searchservice "$AZURE_SEARCH_SERVICE" --index "$AZURE_SEARCH_INDEX" --formrecognizerservice "$AZURE_FORMRECOGNIZER_SERVICE" --tenantid "$AZURE_TENANT_ID" --embeddingendpoint "$AZURE_OPENAI_EMBEDDING_ENDPOINT"
