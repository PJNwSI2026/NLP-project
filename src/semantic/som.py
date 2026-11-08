"""Kohonen Self-Organizing Map (SOM) implementation in NumPy.
Configured with exactly 50 neurons (5x10 2D lattice) for semantic clustering.
"""

from typing import Dict, List, Optional, Tuple
import numpy as np


class KohonenSOM:
    """Self-Organizing Map (SOM) with competitive learning and Gaussian neighborhood."""

    def __init__(
        self,
        grid_rows: int = 5,
        grid_cols: int = 10,
        input_dim: int = 100,
        initial_lr: float = 0.5,
        final_lr: float = 0.02,
        initial_radius: float = 3.5,
        final_radius: float = 0.5,
        random_state: Optional[int] = 42,
    ):
        self.rows = grid_rows
        self.cols = grid_cols
        self.num_neurons = grid_rows * grid_cols
        assert self.num_neurons == 50, f"Professor requirement: exactly 50 neurons, got {self.num_neurons}"

        self.input_dim = input_dim
        self.initial_lr = initial_lr
        self.final_lr = final_lr
        self.initial_radius = initial_radius
        self.final_radius = final_radius
        self.random_state = random_state

        if random_state is not None:
            np.random.seed(random_state)

        # Precompute 2D grid coordinates for fast vectorized distance calculations
        # shape: (rows, cols, 2)
        r_coords, c_coords = np.meshgrid(np.arange(self.rows), np.arange(self.cols), indexing="ij")
        self.grid_coords = np.stack([r_coords, c_coords], axis=-1).astype(np.float64)

        # Initialize weights: random uniform normalized on unit sphere
        self.weights = np.random.uniform(-1.0, 1.0, size=(self.rows, self.cols, self.input_dim))
        self._normalize_weights()

        self.history_quantization_error: List[float] = []

    def _normalize_weights(self):
        """Normalizes each neuron weight vector to unit length."""
        norms = np.linalg.norm(self.weights, axis=-1, keepdims=True)
        norms[norms == 0] = 1.0
        self.weights /= norms

    def find_bmu(self, x: np.ndarray) -> Tuple[int, int]:
        """Finds the coordinates (row, col) of the Best Matching Unit (BMU) for vector x."""
        # Euclidean distance across grid: ||x - W||^2
        diff = self.weights - x  # shape: (rows, cols, input_dim)
        dists = np.sum(diff ** 2, axis=-1)  # shape: (rows, cols)
        flat_idx = np.argmin(dists)
        r, c = np.unravel_index(flat_idx, dists.shape)
        return int(r), int(c)

    def train(self, data: np.ndarray, epochs: int = 80, verbose: bool = True) -> List[float]:
        """Trains the Kohonen SOM using competitive learning and decaying Gaussian neighborhood."""
        num_samples = len(data)
        total_steps = epochs * num_samples
        step = 0

        self.history_quantization_error = []
        if verbose:
            print(f"Training Kohonen SOM (50 neurons: {self.rows}x{self.cols}, input_dim={self.input_dim})...")

        for epoch in range(epochs):
            # Shuffle dataset each epoch
            indices = np.random.permutation(num_samples)

            for idx in indices:
                x = data[idx]

                # 1. Competitive phase: Find BMU
                bmu_r, bmu_c = self.find_bmu(x)

                # 2. Decaying learning rate and neighborhood radius
                progress = step / float(total_steps)
                lr = self.initial_lr * (self.final_lr / self.initial_lr) ** progress
                radius = self.initial_radius * (self.final_radius / self.initial_radius) ** progress

                # 3. Cooperative phase: Gaussian neighborhood on 2D grid
                bmu_pos = np.array([bmu_r, bmu_c], dtype=np.float64)
                grid_dist_sq = np.sum((self.grid_coords - bmu_pos) ** 2, axis=-1)  # shape: (rows, cols)
                h = np.exp(-grid_dist_sq / (2.0 * (radius ** 2)))  # shape: (rows, cols)

                # 4. Adaptive phase: Vectorized weight update
                # delta_w = lr * h[:, :, None] * (x - W)
                update = lr * h[:, :, np.newaxis] * (x - self.weights)
                self.weights += update

                step += 1

            self._normalize_weights()

            # Record quantization error periodically
            if (epoch + 1) % 10 == 0 or epoch == 0 or epoch == epochs - 1:
                qe = self.quantization_error(data)
                self.history_quantization_error.append(qe)
                if verbose:
                    print(f"  Epoch {epoch+1:3d}/{epochs} - Quantization Error: {qe:.4f}")

        return self.history_quantization_error

    def quantization_error(self, data: np.ndarray) -> float:
        """Computes the average Euclidean distance between each data vector and its BMU."""
        total_dist = 0.0
        for x in data:
            r, c = self.find_bmu(x)
            total_dist += np.linalg.norm(x - self.weights[r, c])
        return total_dist / len(data)

    def topographic_error(self, data: np.ndarray) -> float:
        """Computes topographic error: proportion of vectors whose 1st and 2nd BMUs are not neighbors."""
        err_count = 0
        for x in data:
            diff = self.weights - x
            dists = np.sum(diff ** 2, axis=-1)
            flat_sorted = np.argsort(dists.ravel())

            bmu1 = np.unravel_index(flat_sorted[0], dists.shape)
            bmu2 = np.unravel_index(flat_sorted[1], dists.shape)

            # Check Chebyshev or Manhattan adjacency
            r_diff = abs(bmu1[0] - bmu2[0])
            c_diff = abs(bmu1[1] - bmu2[1])
            if max(r_diff, c_diff) > 1:
                err_count += 1
        return err_count / len(data)

    def compute_u_matrix(self) -> np.ndarray:
        """Computes the Unified Distance Matrix (U-Matrix).
        
        For each neuron, computes the average distance to its 4-connected (or 8-connected) neighbors.
        Higher values represent cluster boundaries, lower values represent cluster centers.
        """
        u_matrix = np.zeros((self.rows, self.cols), dtype=np.float64)

        for r in range(self.rows):
            for c in range(self.cols):
                neighbor_dists = []
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        d = np.linalg.norm(self.weights[r, c] - self.weights[nr, nc])
                        neighbor_dists.append(d)
                u_matrix[r, c] = np.mean(neighbor_dists)

        return u_matrix

    def map_data(self, data: np.ndarray) -> Tuple[Dict[Tuple[int, int], List[int]], np.ndarray]:
        """Maps dataset samples to BMU neurons.
        
        Returns:
            assignments: dict mapping (row, col) -> list of sample indices
            activation_map: 2D array (rows, cols) containing sample counts per neuron
        """
        assignments: Dict[Tuple[int, int], List[int]] = {
            (r, c): [] for r in range(self.rows) for c in range(self.cols)
        }
        activation_map = np.zeros((self.rows, self.cols), dtype=np.int32)

        for i, x in enumerate(data):
            r, c = self.find_bmu(x)
            assignments[(r, c)].append(i)
            activation_map[r, c] += 1

        return assignments, activation_map

