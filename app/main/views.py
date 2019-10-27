from flask import render_template,redirect,url_for, abort,request,flash
from . import main
from ..requests import get_quotes
from .forms import CommentsForm, UpdateProfile, BlogForm
from ..models import User,Blog, Comment, Blog
from flask_login import login_required, current_user
from .. import db, photos
import markdown2

    

# Views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    posts = Blog.query.order_by(Blog.date).all()
    quotes = get_quotes()

    title = 'Home - Welcome to the bloging site'
    return render_template('index.html', title = title, quotes = quotes, posts=posts)

@main.route('/about')
def about():
    '''
    View root page function that returns the about page and its data
    '''
    title = ''
    return render_template('about.html', title=title)

@main.route('/post/<int:post_id>')
def post(post_id):
    '''
    View root page function that returns the posts page and its data
    '''
    post = Blog.query.filter_by(id=post_id).one()
    post_comments = Comment.get_comments(post_id)
    title = ''
    return render_template('post.html', title = title, post=post, post_comments=post_comments )

@main.route('/contact')
def contact():
    '''
    View root page function that returns the contact page and its data
    '''
    title = ''
    return render_template('contact.html', title = title)

@main.route('/add',  methods=['GET', 'POST'])
@login_required
def add():
    '''
    View root page function that returns the add post page and its data
    '''
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        subtitle = form.subtitle.data
        content = form.content.data

        new_post = Blog(title=title, subtitle=subtitle, content=content, user=current_user)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add.html', form=form)



@main.route('/pitch/comments/new/<int:id>',methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentsForm()
   
    if form.validate_on_submit():
        new_comment = Comment(blog_id =id,comment=form.comment.data,username=current_user.username)
        new_comment.save_comments()
        return redirect(url_for('main.all'))
    
    return render_template('new_comment.html',comment_form=form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path 
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    
    return render_template('profile/update.html',form =form)

@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Blog.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = BlogForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.content = form.content.data
        
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.subtitle = post.subtitle
        form.content.data = post.content
    return render_template('add.html', title='Update Post', form=form)

@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Blog.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@main.route('/view/comment/<int:id>')
def view_comments(id):
    '''
    Function that returs  the comments belonging to a particular pitch
    '''
    comments = Comment.get_comments(id)
    return render_template('view_comments.html',comments = comments, id=id)




