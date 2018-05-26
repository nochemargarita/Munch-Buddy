def query_user(user):
    """Returns an object of information about the current user in session."""
    user = User.query.filter(User.user_id == user).first()

    return user


def query_message_session(sess, user_id):

    return MessageSession.query.filter(((MessageSession.from_user_id == sess) |
                                       (MessageSession.from_user_id == user_id)) &
                                      ((MessageSession.to_user_id == user_id) |
                                       (MessageSession.to_user_id == sess))).first()


def query_message_of_matches(sess, user_id):
    """Returns a dictionary of messages of current user and his/her matches."""

    all_messages = {}
    messages = Message.query.filter(Message.sess_id == query_message_session(sess, user_id).sess_id).all()

    if messages:
        for message in messages:
            from_user = query_user(message.from_user_id)
            to_user = query_user(message.to_user_id)

            if message.sess_id not in all_messages:
                str_date = message.messaged_on.strftime('%a %b %d')
                all_messages[message.sess_id] = [{'from': from_user.fname,
                                                  'to': to_user.fname,
                                                  'message': message.message,
                                                  'date': str_date}]
            else:
                all_messages[message.sess_id].append({'from': from_user.fname,
                                                      'to': to_user.fname,
                                                      'message': message.message,
                                                      'date': str_date})

    return all_messages


@app.route('/munchbuddies')
def show_buddies():
    """Directs user to a page with list of people who matched his/her choice of categories."""
    sess = session.get('user_id')

    if sess:
        name = session.get('name')
        results = pearson_algorithm.get_all_restaurants(sess)

        matches = {}
        for user_id, restaurant in results.iteritems():
            user = query_user(user_id)
            sess_id = query_message_session(sess, user_id)
            matches[user.user_id] = [user.fname, user.interests, sess_id.sess_id, choice(restaurant), user_id]

        pearson_algorithm.create_session(sess)
        return render_template('munchbuddies.html', matches=matches, sess=sess, name=name, all_messages=all_messages, async_mode=socketio.async_mode)

    else:
        return redirect('/login')
# @app.route('/munchbuddies')
# def show_buddies():
#     """Directs user to a page with list of people who matched his/her choice of categories."""
#     sess = session.get('user_id')

#     if sess:
#         # user = User.query.filter(User.user_id == sess).first()
#         # session['name'] = user.fname
#         name = session.get('name')
#         results = pearson_algorithm.get_all_restaurants(sess)
#         matches = {}
#         all_messages = {}
#         for user_id, restaurant in results.iteritems():
#                 # user = User.query.filter(User.user_id == user_id).first()
#                 # sess_id = MessageSession.query.filter(((MessageSession.from_user_id == sess) |
#                 #                                        (MessageSession.from_user_id == user_id)) &
#                 #                                       ((MessageSession.to_user_id == user_id) |
#                 #                                        (MessageSession.to_user_id == sess))).first()
#                 # messages = Message.query.filter(Message.sess_id == sess_id.sess_id).all()

#                     if messages:
#                         for message in messages: 
#                             from_user_name = User.query.filter(User.user_id == message.from_user_id).first()
#                             to_user_name = User.query.filter(User.user_id == message.to_user_id).first()

#                             if message.sess_id not in all_messages:
#                                 str_date = message.messaged_on.strftime('%a %b %d')
#                                 all_messages[message.sess_id] = [{'from': from_user_name.fname, 'to': to_user_name.fname, 'message': message.message, 'date': str_date}]
#                             else:
#                                 all_messages[message.sess_id].append({'from': from_user_name.fname, 'to': to_user_name.fname, 'message': message.message, 'date': str_date})


#                 matches[user.user_id] = [user.fname, user.interests, sess_id.sess_id, choice(restaurant), user_id]

#         pearson_algorithm.create_session(sess)
#         return render_template('munchbuddies.html', matches=matches, sess=sess, name=name, all_messages=all_messages, async_mode=socketio.async_mode)

#     else:
#         return redirect('/login')


 {1: [{'date': 'Fri May 25', 'to': u'Hannah', 'message': u'THis is tin hannah', 'from': u'Tin'}, {'date': 'Fri May 25', 'to': u'Hannah', 'message': u'hello tin, i am hannah!', 'from': u'Tin'}, {'date': 'Fri May 25', 'to': u'Hannah', 'message': u'OMG, I am tin!', 'from': u'Tin'}, {'date': 'Fri May 25', 'to': u'Hannah', 'message': u"g'", 'from': u'Tin'}, {'date': 'Fri May 25', 'to': u'Hannah', 'message': u'h', 'from': u'Tin'}, {'date': 'Fri May 25', 'to': u'Hannah', 'message': u'k', 'from': u'Tin'}, {'date': 'Fri May 25', 'to': u'Hannah', 'message': u'working', 'from': u'Tin'}, {'date': 'Fri May 25', 'to': u'Tin', 'message': u'h', 'from': u'Hannah'}, {'date': 'Fri May 25', 'to': u'Tin', 'message': u'are', 'from': u'Hannah'}, {'date': 'Fri May 25', 'to': u'Tin', 'message': u' you', 'from': u'Hannah'}, {'date': 'Fri May 25', 'to': u'Tin', 'message': u'are you', 'from': u'Hannah'}]}






