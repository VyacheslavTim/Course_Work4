from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service
from decorator import auth_required, admin_required


director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        page = request.args.get("page")

        filters = {
            "page": page
        }

        rs = director_service.get_all(filters)
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        request_json = request.json
        director_service.create(request_json)
        return "", 201


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, rid):
        request_json = request.json
        if "id" not in request_json:
            request_json["id"] = rid

        director_service.update(request_json)
        return "", 204

    @admin_required
    def delete(self, rid):
        director_service.delete(rid)
        return "", 204
