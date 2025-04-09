class Storage:
    def __inti__(self) -> None:
        self._assistant_id: str = None

    def __set__(self, value: str) -> None:
        self._assistant_id = value

    def __get__(self) -> None | str:
        if not self._assistant_id:
            raise RuntimeError("The assistant id is not set")
        return self._assistant_id
