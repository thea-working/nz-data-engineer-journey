from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineSettings:
    project_root: Path
    top_n_content: int = 10

    @classmethod
    def from_project_root(
        cls, project_root: str | Path, top_n_content: int = 10
    ) -> "PipelineSettings":
        return cls(project_root=Path(project_root), top_n_content=top_n_content)

    @property
    def data_dir(self) -> Path:
        return self.project_root / "data"

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def silver_dir(self) -> Path:
        return self.data_dir / "silver"

    @property
    def gold_dir(self) -> Path:
        return self.data_dir / "gold"

    @property
    def quality_dir(self) -> Path:
        return self.data_dir / "quality"

    @property
    def raw_events_path(self) -> str:
        return str(self.raw_dir / "user_events.parquet")

    @property
    def raw_users_path(self) -> str:
        return str(self.raw_dir / "users.parquet")

    @property
    def raw_content_path(self) -> str:
        return str(self.raw_dir / "content.parquet")

    @property
    def cleaned_events_path(self) -> str:
        return str(self.silver_dir / "cleaned_events.parquet")

    @property
    def enriched_events_path(self) -> str:
        return str(self.silver_dir / "enriched_events.parquet")

    @property
    def sessionized_events_path(self) -> str:
        return str(self.silver_dir / "sessionized_events.parquet")

    @property
    def session_metrics_path(self) -> str:
        return str(self.gold_dir / "session_metrics.parquet")

    @property
    def daily_active_users_path(self) -> str:
        return str(self.gold_dir / "daily_active_users.parquet")

    @property
    def user_engagement_path(self) -> str:
        return str(self.gold_dir / "user_engagement.parquet")

    @property
    def content_ranking_path(self) -> str:
        return str(self.gold_dir / "content_ranking.parquet")

    @property
    def quality_report_path(self) -> str:
        return str(self.quality_dir / "quality_report.json")

    def ensure_directories(self) -> None:
        for path in (
            self.raw_dir,
            self.silver_dir,
            self.gold_dir,
            self.quality_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)
