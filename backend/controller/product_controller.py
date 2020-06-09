import pymysql

from flask      import request, g
from connection import get_connection
from utils      import authorize

def create_product_endpoints(app, product_service):
    product_service = product_service

    @app.route('/product', methods=['POST'])
    @authorize
    def product_register():
        # 상품 등록 API

        db_connection = None
        product_infos = request.json
        try:
            db_connection = get_connection()
            if db_connection:
                product_infos['seller_id'] = g.user
                register_response = product_service.create_new_product(product_infos, db_connection)
                db_connection.commit()
                return register_response

        except pymysql.err.InternalError as e:
            return {'message': 'DATABASE_SERVER_ERROR' + str(e)}, 500

        except pymysql.err.OperationalError:
            return {'message': 'DATABASE_ACCESS_DENIED'}, 500

        except pymysql.err.ProgrammingError as e:
            return {'message': 'DATABASE_PROGRAMMING_ERROR' + str(e)}, 500

        except pymysql.err.NotSupportedError:
            return {'message': 'DATABASE_NOT_SUPPORTED_ERROR'}, 500

        except pymysql.err.IntegrityError as e:
            return {'message': 'DATABASE_INTERGRITY_ERROR' + str(e)}, 500

        except Exception as e:
            db_connection.rollback()
            return {'message': str(e)}, 500

        finally:
            if db_connection:
                db_connection.close()

    @app.route('/product/sellers', methods = ['GET'])
    @authorize
    def get_seller_list():
        # 마스터 상품 등록 시 셀러 리스트 찾기
        db_connection = None
        try:
            db_connection = get_connection()
            if db_connection:
                sellers_kor_names = product_service.sellers_kor_names(g.user, db_connection)
                return {"sellers" : sellers_kor_names}, 200

        except pymysql.err.InternalError as e:
            return {'message': 'DATABASE_SERVER_ERROR' + str(e)}, 500

        except pymysql.err.OperationalError:
            return {'message': 'DATABASE_ACCESS_DENIED'}, 500

        except pymysql.err.ProgrammingError as e:
            return {'message': 'DATABASE_PROGRAMMING_ERROR' + str(e)}, 500

        except pymysql.err.NotSupportedError:
            return {'message': 'DATABASE_NOT_SUPPORTED_ERROR'}, 500

        except pymysql.err.IntegrityError as e:
            return {'message': 'DATABASE_INTERGRITY_ERROR' + str(e)}, 500

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            if db_connection:
                db_connection.close()

    @app.route('/product/category', methods=['GET'])
    @authorize
    def get_product_first_category():
        db_connection = None

        try:
            db_connection = get_connection()
            if db_connection:
                user = {}
                user['user'] = g.user
                register_response = product_service.get_product_first_categories(user, db_connection)
                return register_response

        except pymysql.err.InternalError as e:
            return {'message': 'DATABASE_SERVER_ERROR' + str(e)}, 500

        except pymysql.err.OperationalError:
            return {'message': 'DATABASE_ACCESS_DENIED'}, 500

        except pymysql.err.ProgrammingError as e:
            return {'message': 'DATABASE_PROGRAMMING_ERROR' + str(e)}, 500

        except pymysql.err.NotSupportedError:
            return {'message': 'DATABASE_NOT_SUPPORTED_ERROR'}, 500

        except pymysql.err.IntegrityError as e:
            return {'message': 'DATABASE_INTERGRITY_ERROR' + str(e)}, 500

        except Exception as e:
            db_connection.rollback()
            return {'message': str(e)}, 500

        finally:
            if db_connection:
                db_connection.close()

    @app.route('/resize', methods=['POST'])
    def resize_image():
        db_connection = None
      
        db_connection = get_connection()
        if db_connection:
            image_url = '/home/sungjunjin/바탕화면/brandi.jpg'
            register_response = product_service.resize_image(image_url, db_connection)
            return image_url

    @app.route('/products', methods=['GET'])
    @authorize
    def get_product_list():

        if g.auth is not 1:
            return {'message' : 'UNAUTHORIZED'}, 401

        db_connection = None
        try:
            db_connection = get_connection()
            if db_connection:
                products = product_service.get_product_list(db_connection)

                # if 400 in products:
                #     return products

                # return {'number_of_sellers' : len(products),
                #             'number_of_pages' : int(len(products)/10)+1,
                #             'sellers' : products,
                #             }, 200

                return products

        except pymysql.err.InternalError:
            return {'message': 'DATABASE_SERVER_ERROR'}, 500

        except pymysql.err.OperationalError:
            return {'message': 'DATABASE_ACCESS_DENIED'}, 500

        except pymysql.err.ProgrammingError:
            return {'message': 'DATABASE_PROGRAMMING_ERROR'}, 500

        except pymysql.err.NotSupportedError:
            return {'message': 'DATABASE_NOT_SUPPORTED_ERROR'}, 500

        except pymysql.err.IntegrityError:
            return {'message': 'DATABASE_INTERGRITY_ERROR'}, 500

        except  Exception as e:
            return {'message': str(e)}, 500

        finally:
            if db_connection:
                db_connection.close()