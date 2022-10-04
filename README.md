# UnShort - Link

This is a simple web-app that UnShortens shortened link.

It can be Self-Hosted.

It is built with [FastApi](https://fastapi.tiangolo.com/) and deployed on [Vercel](https://vercel.com/)

## Setup

1. Clone the repository
2. Make a virtualenv

    ```sh
    virtualenv 3.8.5 #can use any environment
    ```

3. Install requirements

    ```sh
    pip install -r requirements.txt
    ```

4. Run it

    ```sh
    uvicorn app:app --reload
    ```

5. It's done. You can deploy it anywhere

## Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/sarvesh4396/unshortener)
