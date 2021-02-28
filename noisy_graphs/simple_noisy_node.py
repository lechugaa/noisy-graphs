class NoisyNode:
    def __init__(self, value, desired_ftrp, real_connections, fake_connections):
        self.__value = value
        self.__desired_ftrp = desired_ftrp
        self.__set_connections(real_connections, fake_connections)

    def __set_connections(self, real_connections, fake_connections):

        self.__real_connections = real_connections
        self.__fake_connections = fake_connections

        self.__set_fake_to_real_proportion()
        self.__set_sigma()

    def __set_fake_to_real_proportion(self):
        self.__ftrp = self.__fake_connections / self.__real_connections

    def __set_sigma(self):
        self.__sigma = self.__ftrp / self.__desired_ftrp

    def set_connections(self, real_connections, fake_connections):
        self.__set_connections(real_connections, fake_connections)

    def increment_connections(self, delta_real=0, delta_fake=0):
        self.__real_connections += delta_real
        self.__fake_connections += delta_fake

    @property
    def value(self):
        return self.__value

    @property
    def connections(self):
        return self.__real_connections, self.__fake_connections

    @property
    def desired_ftrp(self):
        return self.__ftrp

    @property
    def ftrp(self):
        return self.__ftrp

    @property
    def sigma(self):
        return self.__sigma

    def __str__(self):
        return self.__value

    def __repr__(self):
        return f"{self.__value} – ({self.__ftrp}, {self.__sigma})"

    def __eq__(self, other):
        if not isinstance(other, NoisyNode):
            return False
        return self.__value == other.__value

    def __hash__(self):
        return hash(self.__value)

    def __lt__(self, other):
        return self.__sigma < other.__sigma

    def __le__(self, other):
        return self.__sigma <= other.__sigma

    def __gt__(self, other):
        return self.__sigma > other.__sigma

    def __ge__(self, other):
        return self.__sigma >= other.__sigma

    def __neg__(self):
        return NoisyNode(self.__value, self.__desired_ftrp, -self.__real_connections, self.__fake_connections)
