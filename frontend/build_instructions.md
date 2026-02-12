## INSTRUCTIONS
### LOCAL BUILD
1. Make sure to have Docker running
2. Go to frontend/ folder
3. Run command `docker build -t grammy .`
4. Run command `docker run -p 5173:5173 grammy`

### DEPLOYMENT
1. Make sure to have Docker running
2. Go to frontend/ folder
3. Run command `docker build -t grammy .`
4. Run command `docker run --rm -v "/$(pwd)/dist:/out" grammy sh -c "npm run build && cp -r dist/* /out"`
5. Go to infrastructure/grammy
6. Run command `cdk deploy`