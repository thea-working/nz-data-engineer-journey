import pandas as pd
import logging

logger = logging.getLogger(__name__)


class APIPostPipeline:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.df = None
        self.df_user_posts = None

    def load_data(self):
        """
        Load API json data
        :return: pd.DataFrame
                 user posts dataset
        """
        logger.info('Loading API json data')
        self.df = pd.read_json(self.input_file)
        logger.info('Loaded %d rows', len(self.df))

    def compute_user_posts_count(self):
        """
        Aggregate user posts by user_id
        :return: df_user_post pd.Dataframe with columns
                 user_id
                 post_count
        """
        if self.df is None:
            raise ValueError('No data loaded')
        logger.info('Computing user posts count')
        result = (
            self.df.groupby('userId')
            .agg(post_count=('id', 'count'))
            .reset_index()
        )

        self.df_user_posts = result
        logger.info('Created user post summary (%d rows)', len(self.df_user_posts))

    def save_result(self):
        """
        Save user posts to csv file
        :return: None
        """
        self.output_file.mkdir(parents=True, exist_ok=True)
        output_file = self.output_file / 'user_posts.csv'
        logger.info('Saving user post summary to %s', output_file)

        self.df_user_posts.to_csv(output_file, index=False)

        logger.info('Saved %d records', len(self.df_user_posts))

    def run(self):
        # extract
        self.load_data()

        # aggregate
        self.compute_user_posts_count()

        # output
        self.save_result()
