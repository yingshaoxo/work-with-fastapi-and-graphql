# docker build --tag yingshaoxo/python_building_test .

FROM python:3.10-bullseye as python_builder 
COPY . /work_space
WORKDIR /work_space
RUN bash build.sh

FROM ubuntu:focal
COPY --from=python_builder /work_space/program.run /bin/program.run

WORKDIR /bin

EXPOSE 1111

CMD ["/bin/program.run"]
