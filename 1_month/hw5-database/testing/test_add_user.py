import datetime

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

import db

db.main()


def tests():
    alex_posts = add_data()
    select_posts(alex_posts)


def add_data():
    # users
    alex = db.User(username='alex',
                   password='1234')
    ellie = db.User(username='ellie',
                    password='1234')
    mikle = db.User(username='mikle',
                    password='1234')

    session = Session(db.engine)
    session.add_all((alex, ellie, mikle))
    session.commit()

    # tags
    meeting_tag = db.Tag(name='meeting')
    news_tag = db.Tag(name='news')
    monopoly_tag = db.Tag(name='monopoly')

    session.add_all((meeting_tag, news_tag, monopoly_tag))

    # posts
    news_post = db.Post(title='Atention!',
                        description='Very good news',
                        text='Hello, world!',
                        create_data=datetime.datetime.now(),
                        owner_id=alex.id)
    game_post = db.Post(title='New game!',
                        description='new monopoly version was presented',
                        text='Hobby World was present new monopoly about...',
                        create_data=datetime.datetime.now(),
                        owner_id=alex.id)
    session.add_all(
        [news_post,
         game_post]
    )
    session.commit()

    # link posts
    stmt = insert(db.association_table).values([
        {
            db.association_table.c.post_id: news_post.id,
            db.association_table.c.tag_id: news_tag.id
        },
        {
            db.association_table.c.post_id: game_post.id,
            db.association_table.c.tag_id: news_tag.id
        },
        {
            db.association_table.c.post_id: game_post.id,
            db.association_table.c.tag_id: monopoly_tag.id
        },
    ])

    with db.engine.connect() as connection:
        with connection.begin():
            connection.execute(stmt)

    return [str(news_post), str(game_post)]


def select_posts(alex_posts):
    stmt = select(db.Post).where(db.Post.owner_id == 1).order_by(db.Post.id)

    session = Session(db.engine)
    assert [str(post) for post in session.scalars(stmt).all()] == alex_posts
