import uvicorn


def main() -> None:
    uvicorn.run(
        "src.main.server.server:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
    )


if __name__ == "__main__":
    main()
