import torch

from .generalized_abundance import GeneralizedAbundanceGenerator


class YuleAbundance(GeneralizedAbundanceGenerator):
    """
    Optimized generator for abundance counts according to Birth-Death model

    - lda: Probability of copying/reproduction
    - mu: Probability of death
    - LDA: Fixed at 0 (no new independent trees)
    - gamma: Fixed at 0 (no speciation)

    Constraints: lda > mu
    """

    def __init__(self, n_init, Nact, Ninact, max_pop):
        self.param_count = 4
        super().__init__(n_init, Nact, Ninact, max_pop)

    def _extract_params(self, params):
        # TODO: Check where the params are generated and see if the data type
        # can be replaced by something more stable (dataclass, Pydantic model,
        # namedtuple, etc.)
        if isinstance(params, torch.Tensor):
            LDA = params[0].item()
            lda = params[1].item()
            gamma = params[2].item()
            mu = params[3].item()
        elif isinstance(params, dict):
            LDA = params["LDA"]
            mu = params["mu"]
            lda = params["lda"]
            gamma = params["gamma"]
        else:
            LDA = params[0]
            lda = params[1]
            gamma = params[2]
            mu = params[3]
            try:
                if not isinstance(LDA, float) and hasattr(LDA, "__getitem__"):
                    LDA = LDA[0]
                    lda = lda[0]
                    gamma = gamma[0]
                    mu = mu[0]
            except Exception:
                pass
        return {"LDA": LDA, "lda": lda, "mu": mu, "gamma": gamma}
