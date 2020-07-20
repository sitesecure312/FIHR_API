from FHIRstats import *
import sys

def main():

    cls = FIHR_stats()
    cls.load_stats("records_unique.json")

    cls.stats_to_df()

    cls.df['metrics'] = cls.df.apply(map_metrics, axis=1)
    cls.df['applies_datetime'] = cls.df.apply(parse_iso8601_date, axis=1, args=("content.appliesDateTime",) )
    cls.df['applies_period_start'] = cls.df.apply(parse_iso8601_date, axis=1, args=("content.appliesPeriod.start",) )
    cls.df.to_csv("records_unique.csv")

if __name__ == '__main__':
        sys.exit(main())