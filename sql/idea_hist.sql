with 
    frame_stats as (
        select
            min(%s) as min,
            max(%s) as max
        from frame
    ),
    histogram as (
        select
            width_bucket(%s, min, max, 12) as bucket,
            numrange(min(%s)::numeric, max(%s)::numeric, '[]') as range,
            count(*) as freq
        from frame, frame_stats
        group by bucket
        order by bucket
    )
select
    range,
    freq,
    repeat('■', ( freq::float / max(freq) over() * 30 )::int) as bar
from histogram
